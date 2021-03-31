import unittest
from bot_dip import BotDip


class BotDipTest(unittest.TestCase):

    PRICE_TO_BUY = 1.20088999
    EVENT_TIME = 123123112
    PRICE_NOT_TO_BUY = 1.20598
    STOP_LOSS_PRICE = 1.20015745
    PRICE_TO_PROFIT = 1.2059593999999998
    """ABOVE VALUES ARE BASED ON setUp()"""

    def setUp(self) -> None:
        curr_price: float = 1.20599
        pct_drop_for_bid: float = 0.42289
        pct_drop_for_activated_and_bid: float = 0.60
        event_time: int = 123123123  # epoch
        bid_lifespan: int = 3
        stop_loss_pct: float = 0.061
        sell_lifespan: int = 5

        self.bot = BotDip(
            curr_price,
            pct_drop_for_bid,
            pct_drop_for_activated_and_bid,
            event_time,
            bid_lifespan,
            stop_loss_pct,
            sell_lifespan
        )

    """BUYING START"""

    def test_bot_buy(self):

        self.bot.act_on_price(BotDipTest.PRICE_TO_BUY, BotDipTest.EVENT_TIME)
        self.assertTrue(self.bot.has_bought_coin)

    def test_bot_not_buy(self):

        self.bot.act_on_price(BotDipTest.PRICE_NOT_TO_BUY, BotDipTest.EVENT_TIME)
        self.assertFalse(self.bot.has_bought_coin)

    """BUYING END"""

    """SELLING START"""

    def test_bot_should_sell_stop_loss(self):

        self.bot.act_on_price(BotDipTest.PRICE_TO_BUY, BotDipTest.EVENT_TIME)  # buy
        self.bot.act_on_price(BotDipTest.STOP_LOSS_PRICE, BotDipTest.EVENT_TIME)
        self.assertEqual(self.bot.get_status, BotDip.REASON_STOP_LOSS)

    def test_bot_should_sell_profit(self):

        self.bot.act_on_price(BotDipTest.PRICE_TO_BUY, BotDipTest.EVENT_TIME)  # buy
        self.bot.act_on_price(BotDipTest.PRICE_TO_PROFIT, BotDipTest.EVENT_TIME)
        self.assertEqual(self.bot.get_status, BotDip.REASON_PROFIT)

    def test_bot_should_sell_expired(self):

        self.bot.act_on_price(BotDipTest.PRICE_TO_BUY, BotDipTest.EVENT_TIME)  # buy

        for i in range(self.bot.get_life_span + 1):
            # bot will not sell at this price
            self.bot.act_on_price(BotDipTest.STOP_LOSS_PRICE + 0.00001, BotDipTest.EVENT_TIME)

        self.assertEqual(self.bot.get_status, BotDip.REASON_EXPIRED)

    def test_bot_should_not_sell(self):

        self.bot.act_on_price(BotDipTest.PRICE_TO_BUY, BotDipTest.EVENT_TIME)
        self.assertIsNone(self.bot.should_sell(BotDipTest.STOP_LOSS_PRICE + 0.00001))

    """SELLING END"""

    def test_price_to_bid(self):
        self.assertEqual(self.bot.get_price_to_bid, round(1.20088998889, BotDip.BINANCE_FLOATING_POINT))

    """COMPARISON START"""
    @unittest.skip("no comparisons needed for now")
    def test_bot_eq(self):
        test_price = 1.20599
        percentage_change = 0.042289
        event_time = 123123123
        b1 = BotDip(test_price, percentage_change, event_time)
        b2 = BotDip(test_price, percentage_change, event_time)

        self.assertEqual(b1, b2)

    @unittest.skip("no comparisons needed for now")
    def test_bot_lt(self):
        test_price = 1.20599
        percentage_change = 0.042289
        event_time = 123123123
        lesser = BotDip(test_price, percentage_change, event_time)
        greater = BotDip(test_price, percentage_change, event_time)
        greater.act_on_price(0.5, event_time)  # extends life span
        self.assertTrue(lesser < greater)

    @unittest.skip("no comparisons needed for now")
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
        for i in range(self.bot.get_life_span + 1):
            self.bot.act_on_price(BotDipTest.PRICE_TO_BUY + 1, BotDipTest.EVENT_TIME)
        self.assertTrue(self.bot.should_destroy)

    def test_bot_destroy_coin_sold(self):

        self.bot.act_on_price(BotDipTest.PRICE_TO_BUY, BotDipTest.EVENT_TIME)
        self.bot.act_on_price(BotDipTest.PRICE_TO_PROFIT, BotDipTest.EVENT_TIME)
        self.assertTrue(self.bot.should_destroy)

    """DESTROY END"""
