import MetaTrader5 as mt5
import config

"""=================================================================================================================="""


class Terminal:
    """
    Работа с терминалом
    """

    def __init__(self):
        self.login = config.login
        self.password = config.password
        self.server = config.server

    def connect(self):
        # Подключение к MetaTrader 5
        try:
            if not mt5.initialize(login=self.login, password=self.password, server=self.server):
                raise Exception("Ошибка инициализации MT5")
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False

    def disconnect(self):
        # Отключение от MetaTrader 5
        mt5.shutdown()
        print("Инициализация прервана MT5")

    def get_market_data(self, symbol, timeframe, number_of_candles):
        # Получение исторических данных в виде свечей
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, number_of_candles)
        return rates

    def send_order(self, symbol, order_type, volume, price=None, stop_loss=None, take_profit=None):
        # Отправка ордера
        try:
            order_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "price": price,
                "sl": stop_loss,
                "tp": take_profit,
                "deviation": 20,
                "magic": 0,
                "comment": "Python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            result = mt5.order_send(order_request)
            if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
                # noinspection PyUnresolvedReferences
                raise Exception(f'Ошибка отправки ордера: {result.retcode}')
            return result
        except Exception as e:
            print(f"Ошибка при отправке ордера: {e}")
            return None

    def get_account_info(self):
        # Получение информации об аккаунте. """
        return mt5.account_info()._asdict()

    def close_order(self, ticket, volume):
        # Закрытие ордера. """
        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "ticket": ticket,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "position": ticket,
            "deviation": 20,
            "magic": 0,
            "comment": "Python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(close_request)
        return result

    def place_pending_order(self, symbol, order_type, volume, price, stop_loss=None, take_profit=None, expiration=None):
        # Размещение отложенного ордера. """
        pending_order_request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "sl": stop_loss,
            "tp": take_profit,
            "expiration": expiration,
            "deviation": 20,
            "magic": 0,
            "comment": "Python script pending order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(pending_order_request)
        return result

    def delete_pending_order(self, ticket):
        # Удаление отложенного ордера. """
        delete_order_request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "ticket": ticket,
        }
        result = mt5.order_send(delete_order_request)
        return result

    def get_open_positions(self):
        # Получение списка открытых позиций. """
        positions = mt5.positions_get()
        if positions is None:
            return []
        else:
            return positions

    def get_trading_history(self, start_date, end_date):
        # Получение истории торгов за определенный период. """
        history = mt5.history_deals_get(start_date, end_date)
        if history is None or len(history) == 0:
            return []
        else:
            return history

    def modify_order(self, ticket, stop_loss=None, take_profit=None):
        # Изменение параметров ордера. """
        modify_request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "ticket": ticket,
            "sl": stop_loss,
            "tp": take_profit,
        }
        result = mt5.order_send(modify_request)
        return result

    def get_symbol_info(self, symbol):
        # Получение информации о торговом символе. """
        return mt5.symbol_info(symbol)._asdict() if mt5.symbol_info(symbol) is not None else None

    def get_all_symbols(self):
        # Получение списка всех доступных символов. """
        symbols = mt5.symbols_get()
        return [symbol.name for symbol in symbols]

    def get_margin_level(self):
        # Получение текущего уровня маржи. """
        account_info = mt5.account_info()
        return account_info.margin_level if account_info is not None else None

    def check_symbol_trading_conditions(self, symbol):
        # Проверка торговых условий для определенного символа. """
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return None
        return {
            "max_lot_size": symbol_info.volume_max,
            "min_lot_size": symbol_info.volume_min,
            "lot_step": symbol_info.volume_step,
            "trade_allowed": symbol_info.trade_allowed,
            "margin_initial": symbol_info.margin_initial
        }

