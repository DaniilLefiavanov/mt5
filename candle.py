from datetime import datetime


class Candles:
    brithday = datetime.now()

    def __init__(self, timeframe, symbol, time, open, high, low, close):
        self.timeframe = self.tf = timeframe
        self.symbol = self.s = symbol
        self.time = self.t = time
        self.open = self.o = open
        self.high = self.h = high
        self.low = self.l = low
        self.close = self.c = close
        self.color = 'RED' if (open > close) else 'BLUE' if close > open else 'GREY'



