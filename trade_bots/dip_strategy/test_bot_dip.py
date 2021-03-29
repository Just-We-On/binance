import unittest
from bot_dip import BotDip


def test_bot_made_purchase():
    test_price = 1.20599
    percentage_change = 0.042289

    bots = []
    cases = []
    for i in range(len(cases)):
        bot = BotDip(test_price, percentage_change)
        bots.append(bot)


class BotDipTest(unittest.TestCase):

    def test_bot_buy(self):
        test_price = 1.20599
        percentage_change = 0.042289

        prices = [1.20548, 1.20547, 1.10548]

        if len(prices) == 0:
            raise RuntimeError("prices variable need to be set")

        for buy_price in prices:
            bot = BotDip(test_price, percentage_change)
            bot.act_on_price(buy_price)
            self.assertTrue(bot.has_bought_coin)

    def test_bot_not_buy(self):
        test_price = 1.20599
        percentage_change = 0.042289

        prices = [1.20549, 1.20550, 1.20559]

        if len(prices) == 0:
            raise RuntimeError("prices variable need to be set")

        for not_buy_price in prices:
            bot = BotDip(test_price, percentage_change)
            bot.act_on_price(not_buy_price)
            self.assertFalse(bot.has_bought_coin)

    """SELLING START"""

    def test_bot_should_sell_stop_loss(self):
        test_price = 1.20599
        percentage_change = 0.042289

        prices = [1.20497, 1.20496, 1.20172]

        for stop_loss_price in prices:
            bot = BotDip(test_price, percentage_change)
            bot.act_on_price(1.20548)  # buy
            bot.act_on_price(stop_loss_price)
            self.assertEqual(bot.get_status, BotDip.REASON_STOP_LOSS)

    def test_bot_should_sell_profit(self):
        test_price = 1.20599
        percentage_change = 0.042289

        prices = [1.20549, 1.20551, 1.20550]

        for profit_price in prices:
            bot = BotDip(test_price, percentage_change)
            bot.act_on_price(1.20548)  # buy
            bot.act_on_price(profit_price)
            self.assertEqual(bot.get_status, BotDip.REASON_PROFIT)

    def test_bot_should_sell_expired(self):
        test_price = 1.20599
        percentage_change = 0.042289

        price_more_than_willing_to_sell = test_price

        bot = BotDip(test_price, percentage_change)
        bot.act_on_price(1.20548)  # buy

        for i in range(BotDip.LIFE_SPAN_ON_BUY, -1, -1):  # loop backwards
            bot.act_on_price(price_more_than_willing_to_sell)

        self.assertEqual(bot.get_status, BotDip.REASON_EXPIRED)

    def test_bot_should_not_sell(self):
        test_price = 1.20599
        percentage_change = 0.042289

        bot = BotDip(test_price, percentage_change)
        bot.act_on_price(1.20548)  # buy

        prices = [1.20548, 1.20547, 1.20546]

        for not_sell_price in prices:
            self.assertIsNone(bot.should_sell(not_sell_price))
    """SELLING END"""

    def test_price_at_dip(self):
        test_price = 1.20599
        percentage_change = 0.042289
        bot = BotDip(test_price, percentage_change)
        self.assertEqual(bot.get_price_at_dip, 1.20548)
