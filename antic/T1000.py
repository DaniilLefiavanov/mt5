import MetaTrader5 as mt5
import numpy as np
import time
import threading
import multiprocessing
import requests

# Создаем список для хранения логов передачи
log = []
symbol = 'EURUSD'
while True:
    # Получаем массив из трех свечей
    candles = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 3)
    
    # Проверяем, подходят ли свечи под условия
    if are_candles_valid(candles):
        # Если свечи подходят, передаем их другому боту и записываем лог
        other_bot = choose_other_bot()
        log.append({'candles': candles, 'to_bot': other_bot})
    else:
        # Если свечи не подходят, запрашиваем новый массив
        continue
