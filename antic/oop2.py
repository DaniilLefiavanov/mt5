import MetaTrader5 as mt5
import numpy as np
import time

class Bot:
    def __init__(self, symbol):
        mt5.initialize(login=25073081, password="W7vqgEu%38ga", server="Tickmill-Demo")
        self.symbol = symbol; self.timeframe = mt5.TIMEFRAME_H1
        self.array = mt5.copy_rates_from_pos(symbol, self.timeframe, 0, 1000); self.block = self.array[-3:]
        self.current = mt5.copy_rates_from_pos(symbol, self.timeframe, 0, 1); self.tc = self.current[0][0]; self.oc = self.current[0][1]; self.hc = self.current[0][2]; self.lc = self.current[0][3]; self.cc = self.current[0][4]
        self.less = next((less for less in reversed(self.array) if less[3] < self.array[-2][3]), self.array[0]); self.tl = self.less[0]; self.ol = self.less[1]; self.hl = self.less[2]; self.ll = self.less[3]; self.cl = self.less[4]
        self.rl = next((rl for rl in self.array if (self.array[-2][3] < rl[3] < self.array[-3][3]) and (self.tl < rl[0] < self.array[-2][0])), self.array[0]); self.trl = self.rl[0]; self.orl = self.rl[1]; self.hrl = self.rl[2]; self.lrl = self.rl[3]; self.crl = self.rl[4]
        self.more = next((more for more in reversed(self.array) if more[2] > self.array[-2][2]), self.array[0]); self.tm = self.more[0]; self.om = self.more[1]; self.hm = self.more[2]; self.lm = self.more[3]; self.cm = self.more[4]
        self.rm = next((rm for rm in self.array if (self.array[-2][2] > rm[3] > self.array[-3][2]) and (self.tm < rm[0] < self.array[-2][0])), self.array[0]); self.trm = self.rm[0]; self.orm = self.rm[1]; self.hrm = self.rm[2]; self.lrm = self.rm[3]; self.crm = self.rm[4]
        self.t1 = self.block[0][0]; self.o1 = self.block[0][1]; self.h1 = self.block[0][2]; self.l1 = self.block[0][3]; self.c1 = self.block[0][4]
        self.t2 = self.block[1][0]; self.o2 = self.block[1][1]; self.h2 = self.block[1][2]; self.l2 = self.block[1][3]; self.c2 = self.block[1][4]
        self.t3 = self.block[2][0]; self.o3 = self.block[2][1]; self.h3 = self.block[2][2]; self.l3 = self.block[2][3]; self.c3 = self.block[2][4]

    def liqudity(self):
        high_column = [high[2] for high in self.array]; high = [(i, high_column[i]) for i in range(1, len(high_column) - 1) if high_column[i] > high_column[i - 1] and high_column[i] > high_column[i + 1]]
        low_column = [low[3] for low in self.array]; low = [(i, low_column[i]) for i in range(1, len(low_column) - 1) if low_column[i] < low_column[i - 1] and low_column[i] < low_column[i + 1]]
        return "BUY 3 LIQUIDITY" if len(high[-3:]) == 3 and high[-3:][0][1] > high[-3:][1][1] > high[-3:][2][1] else "SELL 3 LIQUIDITY" if len(low[-3:]) == 3 and low[-3:][0][1] < low[-3:][1][1] < low[-3:][2][1] else "NO LIQUIDITY"

    # def BOB(self):
    #     self.bob = self.block; print(f'{self.symbol} BUY ORDER BLOCK {self.t2}')
    #     while True:
    #         if self.bob[-1][0] < self.tc:
    #             self.bob = np.concatenate((self.bob, self.current)); print(f'ADD FOUR CANDLE {self.tc}')
    #         if self.lc > self.lrl and self.hc > self.hrl:
    #             print(f'ACTIVE CANDLE {self.tc}')
    #         if self.liqudity() == "BUY 3 LIQUIDITY":
    #             print(f'{self.liqudity()} ENTER M1 CANDLE {self.bob[0]}')
    #         if self.lc < self.lrl:
    #             print('BLOCK FAILED'); self.bob = self.block; break
    #         else: print('Ожидание активации'); break; time.sleep(1)
    #
    # def BIB(self):
    #     self.bib = self.block; print(f'{self.symbol} BUY INSIDE BAR {self.t2}')
    #     while True:
    #         if self.bib[-1][0] < self.tc: self.bib = np.concatenate((self.bib, self.current)); print(f'ADD FOUR CANDLE {self.tc}')
    #         if self.lc > self.l2 and self.hc > self.h2: print(f'ACTIVE CANDLE {self.tc}')
    #         if self.liqudity() == "BUY 3 LIQUIDITY": print(f'{self.liqudity()} ENTER M1 CANDLE {self.bib[0]}')
    #         if self.lc < self.lrl: print('BLOCK FAILED'); self.bib = self.block; break
    #         else: print('Ожидание активации'); break; time.sleep(1)
    #

    def block_search(self):
        # if (self.l2 < self.l1) and (self.lc > self.l2) and (self.hc > self.h2): return self.BOB()
        # elif (self.l2 < self.l1) and (self.l3 > self.l2) and (self.h3 < self.h2): return self.BIB()
        if (self.h2 > self.h1) and (self.hc < self.h2) and (self.lc < self.l2):
            print(f'{self.symbol} SELL ORDER BLOCK {self.t2}')
            self.sob = self.block
            while True:
                if self.sob[-1][0] < self.tc:
                    self.sob = np.concatenate((self.sob, self.current))
                    print('Добавлена свеча')
                if self.hc < self.hrm and self.lc > self.hrm:
                    print('Блок активировался')
                    print(self.liqudity())
                    print('Запуск функции для минутки')
                    return self.sob
                if self.hc > self.hrm:
                    print('Блок сломан')
                    print('Очищаем массив')
                    break
                else:
                    print('Ожидание активации')
                    break
                    time.sleep(1)
        elif (self.h2 > self.h1) and (self.hc < self.h2) and (self.lc > self.l2):
            print(f'{self.symbol} SELL INSIDE BAR {self.t2}')
            self.sib = self.block
            while True:
                if self.sib[-1][0] < self.tc:
                    self.sib = np.concatenate((self.sib, self.current))
                    print('Добавлена свеча')
                if self.hc < self.h2 and self.lc > self.l2:
                    print('Блок активировался')
                    print(self.liqudity())
                    print('Запуск функции для минутки')
                    return self.sib
                if self.hc > self.h2:
                    print('Блок сломан')
                    print('Очищаем массив')
                    break
                else:
                    print('Ожидание активации')
                    break
                    time.sleep(1)
        else:
            return 'NO TRADE'

EURUSD = bot0 = Bot('EURUSD')
USDCAD = bot1 = Bot('USDCAD')
USDJPY = bot2 = Bot('USDJPY')
AUDUSD = bot3 = Bot('AUDUSD')
NZDUSD = bot4 = Bot('NZDUSD')
XAUUSD = bot5 = Bot('XAUUSD')
EURGBP = bot6 = Bot('EURGBP')
GBPUSD = bot7 = Bot('GBPUSD')
EURJPY = bot8 = Bot('EURJPY')
USDCHF = bot9 = Bot('USDCHF')

print(bot0.symbol, '-', bot0.liqudity())
# print(bot1.symbol, '-', bot1.liqudity())
# print(bot2.symbol, '-', bot2.liqudity())
# print(bot3.symbol, '-', bot3.liqudity())
# print(bot4.symbol, '-', bot4.liqudity())
# print(bot5.symbol, '-', bot5.liqudity())
# print(bot6.symbol, '-', bot6.liqudity())
# print(bot7.symbol, '-', bot7.liqudity())
# print(bot8.symbol, '-', bot8.liqudity())
# print(bot9.symbol, '-', bot9.liqudity())


# print(bot0.symbol, '-', bot0.block_search())
# print(bot1.symbol, '-', bot1.block_search())
# print(bot2.symbol, '-', bot2.block_search())
# print(bot3.symbol, '-', bot3.block_search())
# print(bot4.symbol, '-', bot4.block_search())
# print(bot5.symbol, '-', bot5.block_search())
# print(bot6.symbol, '-', bot6.block_search())
# print(bot7.symbol, '-', bot7.block_search())
# print(bot8.symbol, '-', bot8.block_search())
# print(bot9.symbol, '-', bot9.block_search())