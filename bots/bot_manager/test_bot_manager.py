import unittest
from bot_manager import BotManager


class BotManagerTest(unittest.TestCase):
    def test_win_increment(self):
        test_price = 1.20599
        percentage_change = 0.042289
        event_time = 123123123

        bm = BotManager(percentage_change)
        bm.update_bots_with_curr_price(curr_price=test_price, event_time=event_time)  # buy
        bm.update_bots_with_curr_price(curr_price=1.20548, event_time=event_time + 1)  # buy
        bm.update_bots_with_curr_price(curr_price=1.20550, event_time=event_time + 2)  # sell
        bm.update_bots_with_curr_price(curr_price=1.20550, event_time=event_time + 3)

        self.assertEqual(1, bm.get_win)
