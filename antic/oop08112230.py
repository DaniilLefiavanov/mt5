
import MetaTrader5 as mt5
import time

# Подключаемся к MetaTrader 5
if not mt5.initialize(login=25073081, password=r"W7vqgEu%38ga", server="Tickmill-Demo"):
    print("Не удалось инициализировать MT5")
    mt5.shutdown()


class Robot:

    def __init__(self, symbol):
        """Конструктор."""
        self.symbol = symbol
        self.last_candles = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M1, 0, 3)
        if self.last_candles is not None and len(self.last_candles) >= 3:
            self.t1 = self.last_candles[0][0]; self.h1 = self.last_candles[0][2]; self.l1 = self.last_candles[0][3]
            self.t2 = self.last_candles[1][0]; self.h2 = self.last_candles[1][2]; self.l2 = self.last_candles[1][3]
            self.t3 = self.last_candles[2][0]; self.h3 = self.last_candles[2][2]; self.l3 = self.last_candles[2][3]
        else:
            print("Ошибка: не удалось получить данные свечей.")

    def get_update_candles(self):
        """Обновляем информацию о свечах."""
        current_candle = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M1, 0, 1)
        tc = current_candle[0][0]; hc = current_candle[0][2]; lc = current_candle[0][2]
        if tc != self.t3:
            print(f'tc={tc} t3={robot.t3}')
            self.last_candles[-1] = current_candle
            print(f'self.last_candles[-1]={self.last_candles[-1]} current_candle={current_candle}')
        else:
            self.last_candles = self.last_candles[1:] + [current_candle]
            print(f'self.last_candles={self.last_candles} = self.last_candles[1:]={self.last_candles[1:]}')

    def initialize_block(self):
        """Поиск и распределение блоков."""
        # c1, c2, c3 = self.last_candles
        # BOB = (l2 < l1) and (l3 > l2) and (h3 > h2)  # return 'BUY ORDER BLOCK'
        # BIB = (l2 < l1) and (l3 > l2) and (h3 < h2)  # return 'BUY INSIDE BAR'
        # SOB = (h2 > h1) and (h3 < h2) and (l3 < l2)  # return 'SELL ORDER BLOCK'
        # SIB = (h2 > h1) and (h3 < h2) and (l3 > l2)  # return 'SELL INSIDE BAR'
        # print(BOB, BIB, SOB, SIB)

    def run(self):
        """Основной цикл робота."""
        i = 0
        while True:
            i = i+1
            print(self.get_update_candles())

            print(f'{i} While')
            time.sleep(5)  # Проверяем каждую минуту


# Создаем экземпляр робота для торговли по EURUSD
robot = Robot("EURUSD")
robot.run()

# Завершаем работу с MT5
# mt5.shutdown()









