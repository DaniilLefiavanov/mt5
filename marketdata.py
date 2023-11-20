from terminal import *


"""=================================================================================================================="""

log = EventLog('Bot')

"""=================================================================================================================="""


class Data:

    def __init__(self, symbol):
        self.symbol = symbol
        # self.connect = Terminal(symbol).connect()
        self.array = Terminal(symbol).array()


# data = Data('EURUSD')

# print(data.symbol)
# data.connect

