
class Candles:
    def __init__(self):
        if candle is not None and len(candle) > 0:
            self.t1, self.h1, self.l1 = candle[0][0], candle[0][2], candle[0][3]
        else:
        # Обработка ситуации, когда candle == None или пустой
        candle = mt5.copy_rates_from_pos('EURUSD', mt5.TIMEFRAME_H1, 0, 3)
        self.t1, self.h1, self.l1 = candle[0][0], candle[0][2], candle[0][3]
        self.t2, self.h2, self.l2 = candle[1][0], candle[1][2], candle[1][3]
        self.t3, self.h3, self.l3 = candle[2][0], candle[2][2], candle[2][3]





class Candlestick:
    def __init__(self, timeframe, symbol, time, open, high, low, close):

        self.timeframe = self.tf = timeframe
        self.symbol = self.s = symbol
        self.time = self.t = time
        self.open = self.o = open
        self.high = self.h = high
        self.low = self.l = low
        self.close = self.c = close
        self.color = 'RED' if (open > close) else 'BLUE' if close > open else 'GREY'