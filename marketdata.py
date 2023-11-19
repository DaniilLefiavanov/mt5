
from log import EventLog
from terminal import *

log = EventLog()


class MarketData:

    def __init__(self, name):
        self.log.info(f'{self, name}')
        self.name = name
        self.terminal = Terminal()
        logging.info(f'self.array = {self.terminal}')


market = MarketData('market')

array = market.terminal.market_data('EURUSD', mt5.TIMEFRAME_H1, 0, 1000)
logging.info(f'market')
