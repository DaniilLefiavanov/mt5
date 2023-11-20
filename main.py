import time
import MetaTrader5 as mt5
import config
from terminal import *
from marketdata import *
from robot import *


"""=================================================================================================================="""

bot = Bot('EURUSD')


print(bot.name)
print(bot.array)


"""=================================================================================================================="""

#
# class Candle:                       # Класс Data в нем array а в нем данные свечей
#     def __init__(self, high, low):
#         self.high = high
#         self.low = low
#
# class Block:
#     def __init__(self, type):
#         self.type = type
#
# def create_blocks(candles):
#     blocks = []
#     for i in range(1, len(candles) - 1):
#         L1, H1 = candles[i - 1].low, candles[i - 1].high
#         L2, H2 = candles[i].low, candles[i].high
#         L3, H3 = candles[i + 1].low, candles[i + 1].high
#
#         if L2 < L1 and L3 > L2 and H3 > H2:
#             blocks.append(Block('BOB'))
#         elif L2 < L1 and L3 > L2 and H3 < H2:
#             blocks.append(Block('BIB'))
#         elif H2 > H1 and H3 < H2 and L3 < L2:
#             blocks.append(Block('SOB'))
#         elif H2 > H1 and H3 < H2 and L3 > L2:
#             blocks.append(Block('SIB'))
#
#     return blocks
#
# # Пример использования
# candles = [Candle(high=10, low=5), Candle(high=12, low=4), Candle(high=11, low=6)]
# blocks = create_blocks(candles)
# for block in blocks:
#     print(block.type)