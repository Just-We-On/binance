import unittest
from bot_dip import BotDip


class BotDipTest(unittest.TestCase):

    def test_bot_buy(self):
        test_price = 1.20599
        percentage_change = 0.042289
        event_time = 123123123
        prices = [1.20548, 1.20547, 1.10548]

        if len(prices) == 0:
            raise RuntimeError("prices variable need to be set")

        for buy_price in prices:
            bot = BotDip(test_price, percentage_change, event_time)
            bot.act_on_price(buy_price, event_time)
            self.assertTrue(bot.has_bought_coin)

    def test_bot_not_buy(self):
        test_price = 1.20599
        percentage_change = 0.042289
        event_time = 123123123

        prices = [1.20549, 1.20550, 1.20559]

        if len(prices) == 0:
            raise RuntimeError("prices variable need to be set")

        for not_buy_price in prices:
            bot = BotDip(test_price, percentage_change, event_time)
            bot.act_on_price(not_buy_price, event_time)
            self.assertFalse(bot.has_bought_coin)

    """SELLING START"""

    def test_bot_should_sell_stop_loss(self):
        test_price = 1.20599
        percentage_change = 0.042289
        event_time = 123123123
        prices = [1.20497, 1.20496, 1.20172]

        for stop_loss_price in prices:
            bot = BotDip(test_price, percentage_change, event_time)
            bot.act_on_price(1.20548, event_time)  # buy
            bot.act_on_price(stop_loss_price, event_time)
            self.assertEqual(bot.get_status, BotDip.REASON_STOP_LOSS)

    def test_bot_should_sell_profit(self):
        test_price = 1.20599
        percentage_change = 0.042289
        event_time = 123123123
        prices = [1.20549, 1.20551, 1.20550]

        for profit_price in prices:
            bot = BotDip(test_price, percentage_change, event_time)
            bot.act_on_price(1.20548, event_time)  # buy
            bot.act_on_price(profit_price, event_time)
            self.assertEqual(bot.get_status, BotDip.REASON_PROFIT)

    def test_bot_should_sell_expired(self):
        test_price = 1.20599
        percentage_change = 0.042289
        event_time = 123123123

        bot = BotDip(test_price, percentage_change, event_time)
        bot.act_on_price(1.20548, event_time)  # buy
        not_willing_to_sell_price = 1.20548
        for i in range(BotDip.LIFE_SPAN_ON_BUY):  # loop backwards
            bot.act_on_price(not_willing_to_sell_price, event_time)

        self.assertEqual(bot.get_status, BotDip.REASON_EXPIRED)

    def test_bot_should_not_sell(self):
        test_price = 1.20599
        percentage_change = 0.042289
        event_time = 123123123
        bot = BotDip(test_price, percentage_change, event_time)
        bot.act_on_price(1.20548, event_time)  # buy

        prices = [1.20548, 1.20547, 1.20546]

        for not_sell_price in prices:
            self.assertIsNone(bot.should_sell(not_sell_price))

    """SELLING END"""

    def test_price_at_dip(self):
        test_price = 1.20599
        percentage_change = 0.042289
        event_time = 123123123
        bot = BotDip(test_price, percentage_change, event_time)
        self.assertEqual(bot.get_price_at_dip, 1.20548)

    """COMPARISON START"""

    def test_bot_eq(self):
        test_price = 1.20599
        percentage_change = 0.042289
        event_time = 123123123
        b1 = BotDip(test_price, percentage_change, event_time)
        b2 = BotDip(test_price, percentage_change, event_time)

        self.assertEqual(b1, b2)

    def test_bot_lt(self):
        test_price = 1.20599
        percentage_change = 0.042289
        event_time = 123123123
        lesser = BotDip(test_price, percentage_change, event_time)
        greater = BotDip(test_price, percentage_change, event_time)
        greater.act_on_price(0.5, event_time)  # extends life span
        self.assertTrue(lesser < greater)

    def test_bot_gt(self):
        test_price = 1.20599
        percentage_change = 0.042289
        event_time = 123123123
        lesser = BotDip(test_price, percentage_change, event_time)
        greater = BotDip(test_price, percentage_change, event_time)
        greater.act_on_price(0.5, event_time)  # extends life span
        self.assertTrue(greater > lesser)

    """COMPARISON START"""

    """DESTROY START"""

    def test_bot_destroy_no_coin_purchased(self):
        test_price = 1.20599
        percentage_change = 0.042289
        event_time = 123123123

        not_buy_price = 1.20549
        bot = BotDip(test_price, percentage_change, event_time)
        bot.act_on_price(not_buy_price, event_time)  # not buy
        bot.act_on_price(not_buy_price, event_time)  # not buy
        self.assertTrue(bot.should_destroy)

    def test_bot_destroy_coin_sold(self):
        test_price = 1.20599
        price_willing_to_sell = test_price
        percentage_change = 0.042289
        event_time = 123123123

        bot = BotDip(test_price, percentage_change, event_time)
        bot.act_on_price(1.20548, event_time)
        bot.act_on_price(price_willing_to_sell, event_time)
        self.assertTrue(bot.should_destroy)

    """DESTROY END"""
