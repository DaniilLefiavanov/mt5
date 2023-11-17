import logging


class EventLog:
    """
    Класс для ведения журнала событий, ошибок и торговых операций. Это важно для отладки и анализа работы бота.
    """

    def __init__(self, name, log_file='bot_log.log'):
        # Настройка логгера
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)  # Можно настроить уровень логирования

        # Создание обработчика, который пишет логи в файл
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Создание формата логирования
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Добавление обработчика к логгеру
        self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def debug(self, message):
        self.logger.debug(message)




"""=================================================================================================================="""