from binance_client import client_export
from binance.websockets import BinanceSocketManager
from binance.client import Client
from twisted.internet import reactor
from json import dumps
from signal import signal, SIGINT
from sys import exit


def log_price(msg):
    ''' define how to process incoming WebSocket messages '''

    if msg['e'] != 'error':
        with open('{}.log'.format(msg['s']), 'a') as log_file:
            log_file.write(dumps(msg) + '\n')
            log_file.close()


class Prices:
    SOCKET = "SOCKET"
    CONN_KEY = "CONN_KEY"

    def __init__(self, list_of_coins: list, binance_client: Client) -> None:
        self.socket_manager = {}
        self.binance_client = binance_client
        self.__create_sockets(list_of_coins)

    def __create_sockets(self, list_of_coins: list) -> None:
        for symbol in list_of_coins:
            socket = BinanceSocketManager(self.binance_client)
            self.socket_manager[symbol] = {}
            self.socket_manager[symbol][Prices.SOCKET] = socket

    def get_prices(self):
        for symbol in self.socket_manager:
            socket = self.socket_manager[symbol][Prices.SOCKET]
            self.socket_manager[symbol][Prices.CONN_KEY] = socket.start_symbol_ticker_socket(symbol, log_price)
            socket.start()

    def kill_sockets(self) -> bool:
        if self.socket_manager:
            for symbol in self.socket_manager:
                socket: BinanceSocketManager
                socket = self.socket_manager[symbol][Prices.SOCKET]
                conn_key = self.socket_manager[symbol][Prices.CONN_KEY]
                socket.stop_socket(conn_key)

            self.socket_manager.clear()
            reactor.stop()

            return True

        else:
            return False

    def __del__(self):
        return self.kill_sockets()


def handler(signal_received, frame):
    # Handle any cleanup here
    global prices
    if prices.kill_sockets():
        print('SIGINT or CTRL-C detected. Sockets killed')
    else:
        print('SIGINT or CTRL-C detected. No sockets detected')
    exit(0)


if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    print('Running. Press CTRL-C to exit.')

    coins = "ADA,XLM,XRP,CHZ,MANA".split(',')
    coin_list = [c + "USDT" for c in coins]

    print("obtaining prices for:", coin_list)

    prices = Prices(list_of_coins=coin_list, binance_client=client_export)
    prices.get_prices()
