import unittest
from market import *
import import_data as web

class test_market(unittest.TestCase):
    #helper functions
    def test_next_and_prev_trading_day(self):
        web.import_readable('tsla')
        self.assertEqual(next_trading_day('tsla', '2018-05-26'), '2018-05-29')
        self.assertEqual(next_trading_day('tsla', '2018-05-27'), '2018-05-29')
        self.assertEqual(next_trading_day('tsla', '2018-05-28'), '2018-05-29')
        self.assertEqual(next_trading_day('tsla', '2018-05-29'), '2018-05-29')

        self.assertEqual(prev_trading_day('tsla', '2018-05-26'), '2018-05-25')
        self.assertEqual(prev_trading_day('tsla', '2018-05-27'), '2018-05-25')
        self.assertEqual(prev_trading_day('tsla', '2018-05-28'), '2018-05-25')
        self.assertEqual(prev_trading_day('tsla', '2018-05-29'), '2018-05-29')
        web.remove()
    #Stock class
    def test_stock_constructor(self):
        bp = Stock('bp', '2017-01-01', '2018-03-04')
        self.assertEqual(bp.get_symbol(), 'bp')
        self.assertEqual(bp.get_start_date(), '2017-01-03')
        self.assertEqual(bp.get_end_date(), '2018-03-02')
        self.assertEqual(bp.get_readable().shape[0], 293)
        self.assertEqual(bp.get_readable().shape[1], 5)
    def test_price_open_and_price_close(self):
        dal = Stock('dal', '2018-01-01', '2018-06-03')
        self.assertAlmostEqual(dal.price_open('2018-05-25'), 54.65)
        self.assertAlmostEqual(dal.price_close('2018-05-25'), 55.87)
    def test_percent_change(self):
        intc = Stock('intc', '2018-01-01', '2018-06-01')
        self.assertAlmostEqual(intc.percent_change('2018-06-01'), .0222063)
        self.assertAlmostEqual(intc.percent_change('2018-01-01', '2018-06-01'), .230702889)


if __name__ == '__main__':
    unittest.main()
