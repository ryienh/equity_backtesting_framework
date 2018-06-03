import unittest
from market import *

class test_market(unittest.TestCase):
    def test_stock_constructor(self):
        apple = Stock('aapl', 'yesterday', 'today')
        self.assertEqual(apple.get_symbol(), 'aapl')
        self.assertEqual(apple.get_start_date(), 'yesterday')
        self.assertEqual(apple.get_end_date(), 'today')

if __name__ == '__main__':
    unittest.main()
