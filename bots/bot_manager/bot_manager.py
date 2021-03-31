from bots.dip_strategy.bot_dip import BotDip


class BotManager:

    def __init__(self, pct_change):
        self.__win_count = 0
        self.__lose_count = 0
        self.__inactive_count = 0

        self.__pct_change = pct_change

        self.__bots = {}

        self.__buy_sell_info = []

    @property
    def get_buy_sell_info(self):
        return self.__buy_sell_info

    @property
    def get_bots(self) -> {}:
        return self.__bots

    @property
    def get_win(self) -> int:
        return self.__win_count

    @property
    def get_losses(self) -> int:
        return self.__lose_count

    @property
    def get_inactive(self) -> int:
        return self.__inactive_count

    def get_score(self):
        return "wins: {0}, loss: {1}, inactive: {2}, net score: {3}".format(self.__win_count, self.__lose_count, self.__inactive_count, self.__win_count - self.__lose_count)

    def __add_bot(self, bot: BotDip) -> None:
        self.__bots[bot] = bot

    def update_bots_with_curr_price(self, curr_price: float, event_time: int) -> None:
        bot: BotDip
        for bot_ref in list(self.get_bots.keys()):
            bot = self.__bots[bot_ref]
            if bot.should_destroy:
                reason = bot.get_status
                self.update_score(reason)
                if bot.get_transaction_info:
                    self.__buy_sell_info.append(bot.get_transaction_info)

                del self.__bots[bot_ref]
            else:
                bot.act_on_price(curr_price, event_time)

        new_bot = BotDip(curr_price, self.__pct_change, event_time)
        self.__add_bot(new_bot)

    def update_score(self, reason):
        if reason == BotDip.REASON_PROFIT:
            self.__win_count += 1
        elif reason == BotDip.REASON_STOP_LOSS or reason == BotDip.REASON_EXPIRED:
            self.__lose_count += 1
        elif reason == BotDip.STATUS_INACTIVE:
            self.__inactive_count += 1
        else:
            raise RuntimeError("reason is None")



