
import MetaTrader5 as mt5
import time


# Подключаемся к MetaTrader 5
if not mt5.initialize():
    print("Не удалось инициализировать MT5")
    mt5.shutdown()


class Robot:
    def __init__(self, symbol):
        self.symbol = symbol

    def update_candles(self):
        """Обновляем информацию о свечах."""
        current_candle = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_H1, 0, 1)[0]
        if current_candle['time'] == self.last_candles[-1]['time']:
            self.last_candles[-1] = current_candle
        else:
            self.last_candles = self.last_candles[1:] + [current_candle]

    def run(self):
        """Основной цикл робота."""
        while True:
            if not self.get_last_candles() or not self.compare_candles:
                self.update_candles()
                # Здесь может быть дополнительная логика торговли
            time.sleep(60)  # Проверяем каждую минуту


class Candle:
    def __init__(self):
        self.last_candles = []

    def get_last_candles(self):
        """Получаем три последние часовые свечи."""
        rates = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_H1, 0, 3)
        if rates is not None and len(rates) == 3:
            self.last_candles = rates
            return True
        return False

    def last_three(self):

        """Сравниваем свечи между собой."""
        c = self.last_candles

        self.t1 = c[0][0], self.o1 = c[0][1], self.h1 = c[0][2], self.l1 = c[0][3]
        self.t2 = c[1][0], self.o2 = c[1][1], self.h2 = c[1][2], self.l2 = c[1][3]
        self.t3 = c[2][0], self.o3 = c[2][1], self.h3 = c[2][2], self.l3 = c[2][3]

    def initial_block(self):
        """Определяем блоки."""

        return 'BUY ORDER BLOCK' if (l2 < l1) and (l3 > l2) and (h3 > h2)\
            else 'BUY INSIDE BAR' if (l2 < l1) and (l3 > l2) and (h3 < h2)\
            else 'SELL ORDER BLOCK' if (h2 > h1) and (h3 < h2) and (l3 < l2)\
            else 'SELL INSIDE BAR' if (h2 > h1) and (h3 < h2) and (l3 > l2) else None




# Создаем экземпляр робота для торговли по EURUSD
robot = Robot("EURUSD")
robot.run()

# Завершаем работу с MT5
mt5.shutdown()






#
#
# import time
# import threading
#
# class Candle:
#     def __init__(self, open_price, close_price, high, low):
#         self.open_price = open_price
#         self.close_price = close_price
#         self.high = high
#         self.low = low
#         # Добавьте любые другие атрибуты, которые вам нужны
#
# class Block:
#     def __init__(self, name, candles):
#         self.name = name
#         self.candles = candles
#
#     def analyze_block(self):
#         # Здесь ваша логика анализа блока
#         pass
#
# class Bot:
#     def __init__(self):
#         self.running = True
#
#     def fetch_candles(self):
#         # Здесь ваш код для получения данных о свечах
#         # Верните список из трех объектов Candle
#         return [Candle(1, 2, 3, 4), Candle(2, 3, 4, 5), Candle(3, 4, 5, 6)]
#
#     def identify_block(self, candles):
#         # Здесь ваша логика для определения блока
#         # Верните объект Block
#         return Block("BlockName", candles)
#
#     def process_candles(self):
#         while self.running:
#             candles = self.fetch_candles()
#             block = self.identify_block(candles)
#             if block:
#                 # Если блок найден, передайте его в соответствующую функцию
#                 self.handle_block(block)
#             time.sleep(1)  # Пауза на 1 секунду
#
#     def handle_block(self, block):
#         # Обработайте блок здесь
#         block.analyze_block()
#
#     def start(self):
#         # Запуск бота в отдельном потоке
#         threading.Thread(target=self.process_candles).start()
#
#     def stop(self):
#         self.running = False
#
# # Создание и запуск бота
# bot = Bot()
# bot.start()
#
# # Для остановки бота можно вызвать bot.stop()
#
