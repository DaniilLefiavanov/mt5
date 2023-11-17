import MetaTrader5 as mt5
import numpy as np
import time
import threading

class Bot:
    def __init__(self, symbol):
        mt5.initialize(login=25073081, password="W7vqgEu%38ga", server="Tickmill-Demo")
        self.symbol = symbol; self.timeframe = mt5.TIMEFRAME_H1
        self.array = mt5.copy_rates_from_pos(symbol, self.timeframe, 0, 1000)
        self.block = mt5.copy_rates_from_pos(symbol, self.timeframe, 0, 3)
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

    def search_block(self):
        while True:
            if (self.l2 < self.l1) and (self.l3 > self.l2) and (self.h3 > self.h2): self.bob = self.block; self.buy_ob()
            if (self.l2 < self.l1) and (self.l3 > self.l2) and (self.h3 < self.h2): self.bib = self.block; self.buy_ib()
            if (self.h2 > self.h1) and (self.h3 < self.h2) and (self.l3 < self.l2): self.sob = self.block; self.sell_ob()
            if (self.h2 > self.h1) and (self.h3 < self.h2) and (self.l3 > self.l2): self.sib = self.block; self.sell_ib()
            # time.sleep(10)
            
    def buy_ob(self):
        if len(self.bob) == 3:
            if not self.bob[-1][3] < self.lrl:
                if self.tc == self.bob[-1][0]:
                    if self.hc < self.hrm:
                        print(f'{self.symbol} BUY ORDER BLOCK WAITING') 
                        if self.hc > self.hrm:
                            print(f'{self.symbol} BUY ORDER BLOCK ACTIVE CANDLE {self.tc}')
                            if self.liqudity() == 'BUY 3 LIQUIDITY':
                                print(f'{self.liqudity()} BUY ORDER BLOCK ENTER M1 CANDLE')
                            else: print(f'{self.symbol} BUY ORDER BLOCK NO LIQUIDITY') 
                        else: print(f'{self.symbol} BUY ORDER BLOCK WAITING')
                    else: print(f'{self.symbol} BUY ORDER BLOCK WAITING')
                else: print(f'{self.symbol} BUY ORDER BLOCK ADD FOUR CANDLE {self.tc}'); 
                self.bob = np.concatenate((self.bob, self.current))
            else: print(f'{self.symbol} BUY ORDER BLOCK FAILED')
        else: print(self.bob)

    def buy_ib(self):
        if len(self.bib) == 3:
            if not self.bib[-1][3] < self.l2:
                if self.tc == self.bib[-1][0]:
                    if self.hc < self.h2:
                        print(f'{self.symbol} BUY INSIDE BAR WAITING') 
                        if self.hc > self.hrm:
                            print(f'{self.symbol} BUY INSIDE BAR ACTIVE CANDLE {self.tc}')
                            if self.liqudity() == 'BUY 3 LIQUIDITY':
                                print(f'{self.liqudity()} BUY INSIDE BAR ENTER M1 CANDLE')
                            else: print(f'{self.symbol} BUY INSIDE BAR NO LIQUIDITY')
                        else: print(f'{self.symbol} BUY INSIDE BAR WAITING')
                    else: print(f'{self.symbol} BUY INSIDE BAR WAITING')
                else: print(f'{self.symbol} BUY INSIDE BAR ADD FOUR CANDLE {self.tc}'); 
                self.bib = np.concatenate((self.bib, self.current))
            else: print(f'{self.symbol} BUY INSIDE BAR FAILED')
        else: print(self.bib)

    def sell_ob(self):
        if len(self.sob) == 3:
            if not self.sob[-1][2] > self.hrm:
                if self.tc == self.sob[-1][0]:
                    if self.hc < self.hrm:
                        print(f'{self.symbol} SELL ORDER BLOCK WAITING')
                        if self.lc < self.lrm:                         
                            print(f'{self.symbol} SELL ORDER BLOCK ACTIVE CANDLE {self.tc}')                          
                            if self.liqudity() == 'SELL 3 LIQUIDITY':                           
                                print(f'{self.liqudity()} SELL ORDER BLOCK ENTER M1 CANDLE')                          
                            else: print(f'{self.symbol} SELL ORDER BLOCK NO LIQUIDITY')
                        else: print(f'{self.symbol} SELL ORDER BLOCK WAITING')
                    else: print(f'{self.symbol} SELL ORDER BLOCK WAITING')
                else: print(f'{self.symbol} SELL ORDER BLOCK ADD FOUR CANDLE {self.tc}'); 
                self.sob = np.concatenate((self.sob, self.current))
            else: print(f'{self.symbol} SELL ORDER BLOCK FAILED')
        else: print(self.sob)

    def sell_ib(self):
        if len(self.sib) == 3:
            if not self.sib[-1][2] > self.hrm:
                if self.tc == self.sib[-1][0]:
                    if self.hc < self.hrm:
                        print(f'{self.symbol} SELL INSIDE BAR WAITING')
                        if self.lc < self.lrm:                         
                            print(f'{self.symbol} SELL INSIDE BAR ACTIVE CANDLE {self.tc}')                          
                            if self.liqudity() == 'SELL 3 LIQUIDITY':                           
                                print(f'{self.liqudity()} SELL INSIDE BAR ENTER M1 CANDLE')                          
                            else: print(f'{self.symbol} SELL INSIDE BAR NO LIQUIDITY')
                        else: print(f'{self.symbol} SELL INSIDE BAR WAITING')   
                    else: print(f'{self.symbol} SELL INSIDE BAR WAITING')
                else: print(f'{self.symbol} SELL INSIDE BAR ADD FOUR CANDLE {self.tc}'); 
                self.sib = np.concatenate((self.sib, self.current))
            else: print(f'{self.symbol} SELL INSIDE BAR FAILED')
        else: print(self.sib)

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



EURUSD.search_block()
USDCAD.search_block()
USDJPY.search_block()
AUDUSD.search_block()
NZDUSD.search_block()
XAUUSD.search_block()
EURGBP.search_block()
GBPUSD.search_block()
EURJPY.search_block()
USDCHF.search_block()