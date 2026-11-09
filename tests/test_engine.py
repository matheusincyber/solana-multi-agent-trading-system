import unittest
from pathlib import Path
from simulator.engine import load_candles, simulate, Candle

class EngineTests(unittest.TestCase):
    def test_synthetic_trade_executes(self):
        result = simulate(load_candles(Path('examples/synthetic_candles.csv')))
        self.assertEqual(result['dataset'], 'SYNTHETIC_ONLY')
        self.assertTrue(any(x['side'] == 'BUY' for x in result['orders']))
        self.assertTrue(any(x['side'] == 'SELL' for x in result['orders']))

    def test_no_signal_no_trade(self):
        candles = [Candle(f'2026-11-01T09:0{i}:00Z', 1,1,1,1,1000) for i in range(4)]
        result = simulate(candles)
        self.assertEqual(result['orders'], [])
        self.assertEqual(result['ending_cash'], 90.0)

    def test_max_allocation(self):
        result = simulate(load_candles(Path('examples/synthetic_candles.csv')))
        first_buy = next(x for x in result['orders'] if x['side'] == 'BUY')
        self.assertLessEqual(90-first_buy['cash'], 90*.08+1e-6)

if __name__ == '__main__':
    unittest.main()
