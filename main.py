"""Run the offline synthetic demonstration without external dependencies."""
import argparse
from pathlib import Path
from simulator.engine import load_candles, simulate, export_results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Offline synthetic paper trade simulator')
    parser.add_argument('--candles', type=Path, default=Path('examples/synthetic_candles.csv'))
    parser.add_argument('--output', type=Path, default=Path('output'))
    args = parser.parse_args()
    result = simulate(load_candles(args.candles))
    export_results(result, args.output)
    print(f"{result['dataset']} | orders={len(result['orders'])} | marked equity=${result['marked_equity_before_exit_cost']:.2f}")
    print('Illustrative only. Not real-market results.')
