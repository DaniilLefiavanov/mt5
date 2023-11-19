import MetaTrader5 as mt5

mt5.initialize(login=55571718, password="A4$8iosAn!04", server="live.mt5tickmill.com")
array = mt5.copy_rates_from_pos('EURUSD', mt5.TIMEFRAME_H1, 0, 1)


class Candle:
    def __init__(self, timeframe, symbol, array):

        time, open, high, low, close, *rest = array
        self.timeframe = self.tf = timeframe
        self.symbol = self.s = symbol
        self.time = self.t = time
        self.open = self.o = open
        self.high = self.h = high
        self.low = self.l = low
        self.close = self.c = close
        self.__color = None

    @property
    def color(self):
        if self.__color is None:
            self.__color = 'RED' if self.o > self.c else 'BLUE' if self.c > self.o else 'GREY'
        return self.__color
