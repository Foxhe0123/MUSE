import logging
import colorlog

def get_logger():
    # If the root logger already exists, avoid duplication of configuration
    if len(logging.getLogger().handlers) > 0:
        return logging.getLogger()

    # Set the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set the global log level

    # Create a new log level NOTICE
    NOTICE_LEVEL_NUM = 25
    logging.addLevelName(NOTICE_LEVEL_NUM, "NOTICE")

    # Add a notice method to the Logger class
    def notice(self, message, *args, **kwargs):
        if self.isEnabledFor(NOTICE_LEVEL_NUM):
            self._log(NOTICE_LEVEL_NUM, message, args, **kwargs)

    logging.Logger.notice = notice

    # Create a file handler
    file_handler = logging.FileHandler('logging.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(NOTICE_LEVEL_NUM)

    # Set the log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    debug_formatter = logging.Formatter('%(asctime)s - %(levelname)s -%(funcName)s:%(lineno)d- %(message)s')

    file_handler.setFormatter(debug_formatter)
    console_handler.setFormatter(formatter)

    # Define color output format
    color_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'NOTICE': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'blue',
        }
    )
    # Add color output format to console log handler
    console_handler.setFormatter(color_formatter)
    # Remove the default handler
    for handler in logger.handlers:
        logger.removeHandler(handler)

    # Add the handler to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger




import logging






if __name__ == '__main__':
    logger = get_logger()
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
    logger.notice("This is a notice message.")