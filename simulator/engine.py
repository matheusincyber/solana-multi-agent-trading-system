"""Offline educational paper-trading engine; synthetic data only.

No blockchain, wallet, exchange, or live-price integration.
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import csv
import json
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    initial_cash: float = 90.0
    max_allocation: float = .08
    initial_stop: float = .06
    trailing_activation: float = .12
    trailing_gap: float = .06
    slippage: float = .01
    fee: float = .0035
    cost_per_leg: float = .01
    momentum_threshold: float = .03
    min_volume: float = 100.0
    max_entries_per_day: int = 2
    daily_loss_limit: float = .02
    weekly_loss_limit: float = .05
    max_positions: int = 3

@dataclass(frozen=True)
class Candle:
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume_usd: float

@dataclass
class Position:
    quantity: float
    entry_price: float
    entry_cost: float
    stop_price: float
    highest_high: float
    trailing: bool = False

def simulate(candles: list[Candle], settings: Settings = Settings()) -> dict:
    """Next-candle momentum entries, gap-aware stops, deferred trailing updates."""
    cash = settings.initial_cash
    position: Optional[Position] = None
    orders = []
    entries = {}
    day_start = {}
    week_start = {}
    for i, candle in enumerate(candles):
        day = candle.timestamp[:10]
        iso = datetime.fromisoformat(candle.timestamp.replace('Z', '+00:00')).isocalendar()
        week = f'{iso.year}-W{iso.week:02}'
        day_start.setdefault(day, cash)
        week_start.setdefault(week, cash)
        if position is not None:
            if candle.low <= position.stop_price:
                sell_mark = min(candle.open, position.stop_price)
                fill = sell_mark * (1 - settings.slippage)
                proceeds = position.quantity * fill * (1 - settings.fee) - settings.cost_per_leg
                cash += proceeds
                orders.append({'timestamp': candle.timestamp, 'side': 'SELL', 'price': round(fill, 8),
                               'quantity': round(position.quantity, 8), 'cash': round(cash, 8),
                               'reason': 'stop_or_gap', 'realized_pnl': round(proceeds - position.entry_cost, 8)})
                position = None
            else:
                new_high = max(position.highest_high, candle.high)
                trailing = position.trailing or new_high >= position.entry_price * (1 + settings.trailing_activation)
                new_stop = max(position.stop_price, new_high * (1 - settings.trailing_gap)) if trailing else position.stop_price
                position.highest_high = new_high
                position.trailing = trailing
                position.stop_price = new_stop
        if position is None and i >= 2:
            prev, earlier = candles[i - 1], candles[i - 2]
            date_count = entries.get(day, 0)
            eligible = (prev.close >= earlier.close * (1 + settings.momentum_threshold)
                        and prev.volume_usd >= settings.min_volume and candle.open > 0)
            day_halt = cash < day_start[day] * (1 - settings.daily_loss_limit)
            week_halt = cash < week_start[week] * (1 - settings.weekly_loss_limit)
            if eligible and date_count < settings.max_entries_per_day and not day_halt and not week_halt:
                budget = cash * settings.max_allocation
                buy_fill = candle.open * (1 + settings.slippage)
                quantity = max(0.0, (budget - settings.cost_per_leg) / (buy_fill * (1 + settings.fee)))
                actual_cost = quantity * buy_fill * (1 + settings.fee) + settings.cost_per_leg
                if quantity > 0 and actual_cost <= cash:
                    cash -= actual_cost
                    position = Position(quantity, buy_fill, actual_cost, buy_fill * (1-settings.initial_stop), buy_fill)
                    entries[day] = date_count + 1
                    orders.append({'timestamp': candle.timestamp, 'side': 'BUY', 'price': round(buy_fill, 8),
                                   'quantity': round(quantity, 8), 'cash': round(cash, 8),
                                   'reason': 'prior_candle_momentum', 'realized_pnl': ''})
    last_close = candles[-1].close if candles else 0.0
    marked_value = position.quantity * last_close if position else 0.0
    return {'dataset': 'SYNTHETIC_ONLY', 'starting_cash': settings.initial_cash,
            'ending_cash': round(cash, 8), 'marked_equity_before_exit_cost': round(cash + marked_value, 8),
            'open_position': asdict(position) if position else None, 'orders': orders,
            'note': 'Synthetic illustration, not real-market performance. Marked equity excludes exit costs.'}

def load_candles(path: Path) -> list[Candle]:
    with path.open(newline='', encoding='utf-8') as fp:
        rows = list(csv.DictReader(fp))
    candles = [Candle(timestamp=r['timestamp'], open=float(r['open']), high=float(r['high']),
                      low=float(r['low']), close=float(r['close']), volume_usd=float(r['volume_usd'])) for r in rows]
    for candle in candles:
        if min(candle.open, candle.high, candle.low, candle.close) <= 0 or candle.high < max(candle.open, candle.close) or candle.low > min(candle.open, candle.close):
            raise ValueError('Invalid OHLC candle')
        datetime.fromisoformat(candle.timestamp.replace('Z','+00:00'))
    if [c.timestamp for c in candles] != sorted(set(c.timestamp for c in candles)):
        raise ValueError('Candles must be uniquely timestamped and ordered')
    return candles

def export_results(result: dict, output: Path):
    output.mkdir(parents=True, exist_ok=True)
    (output / 'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    with (output / 'orders.csv').open('w', newline='', encoding='utf-8') as fp:
        columns = ['timestamp','side','price','quantity','cash','reason','realized_pnl']
        writer = csv.DictWriter(fp, fieldnames=columns)
        writer.writeheader()
        writer.writerows(result['orders'])
