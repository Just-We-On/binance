class BotDip:
    REASON_STOP_LOSS = "stop_loss"
    REASON_EXPIRED = "expired"
    REASON_PROFIT = "profit"

    STATUS_INACTIVE = "status-inactive"
    STATUS_PROFIT = "status-profit"
    STATUS_LOSS = "status-loss"

    LIFE_SPAN_ON_BUY = 10

    def __init__(self, curr_price: float, pct_change: float, event_time: int) -> None:
        self.__activated_price: float = round(curr_price, 5)
        self.__price_at_dip: float = round(curr_price * (1 - (pct_change / 100)), 5)
        self.__stop_loss: float = round(self.__price_at_dip * (1 - (pct_change / 100)), 5)

        self.__has_bought_coin: bool = False

        self.__life_span = 1
        self.__status = BotDip.STATUS_INACTIVE
        self.should_destroy = False

        self.__event_time = event_time

        self.__buy_price = None
        self.__buy_time = None
        self.__buy_sell_info = None

    @property
    def get_transaction_info(self):
        return self.__buy_sell_info

    @property
    def get_life_span(self) -> int:
        return self.__life_span

    @property
    def get_price_at_dip(self) -> float:
        return self.__price_at_dip

    @property
    def has_bought_coin(self) -> bool:
        return self.__has_bought_coin

    @property
    def get_stop_loss(self) -> float:
        return self.__stop_loss

    @property
    def get_status(self) -> str:
        return self.__status

    def __eq__(self, other: 'BotDip'):
        return self.get_life_span == other.get_life_span

    def __lt__(self, other: 'BotDip'):
        return self.get_life_span < other.get_life_span

    def __gt__(self, other: 'BotDip'):
        return self.get_life_span > other.get_life_span

    def __hash__(self):
        return hash((self.__activated_price, self.__event_time))

    def should_buy(self, curr_price) -> bool:
        if self.has_bought_coin:
            return False
        return curr_price <= self.get_price_at_dip

    def act_on_price(self, curr_price, event_time) -> None:
        if self.should_destroy:
            return

        if not self.has_bought_coin:
            if self.get_life_span == 0:
                self.should_destroy = True

            elif self.should_buy(curr_price):
                self.buy(curr_price, event_time)
        else:
            reason = self.should_sell(curr_price)
            if reason is None:  # no reason to sell
                pass
            else:
                self.__status = reason
                self.sell(curr_price, event_time)

        self.__life_span -= 1

    def buy(self, buy_price: float, buy_time: int) -> None:
        self.__has_bought_coin = True
        self.__life_span = BotDip.LIFE_SPAN_ON_BUY
        self.__buy_price = buy_price
        self.__buy_time = buy_time

    def should_sell(self, curr_price):
        if curr_price <= self.get_stop_loss:
            return BotDip.REASON_STOP_LOSS

        elif self.get_life_span == 0:
            return BotDip.REASON_EXPIRED

        elif curr_price > self.get_price_at_dip:
            return BotDip.REASON_PROFIT

        else:
            return None

    def sell(self, curr_price: float, sell_time: float) -> None:
        # update score
        self.__life_span = 0
        self.should_destroy = True
        self.__buy_sell_info = {
            'buy_price': self.__buy_price,
            'buy_time': self.__buy_time,
            'sell_price': curr_price,
            'sell_time': sell_time,
            'status': self.get_status
        }
