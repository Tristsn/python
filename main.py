import os
import logging
import sys
from logging import handlers


class Logger:
    level_relations = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARN,
        'ERROR': logging.ERROR,
        'CRIT': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, log_path, log_file_name, log_max_file_size, log_max_file_num, log_out_type, log_level):

        self.__logger = logging.getLogger()
        log_max_file_num = log_max_file_num * 1024 * 1024

        my_path = os.path.join(log_path)
        #   判断路径是否存在
        if not os.path.exists(my_path):
            os.mkdir(my_path)

        #  设置路径
        path = os.path.join(log_path, log_file_name)

        #  设置等级
        self.__level = self.level_relations.get(log_level.upper())
        self.__logger.setLevel(self.__level)

        #  设置字体
        fmt = logging.Formatter('%(asctime)s %(filename)s[%(lineno)d] [%(levelname)s]  %(message)s')

        def __create_log_stream_handler():
            #  控制台输出设置
            log_stream_handler = logging.StreamHandler()
            log_stream_handler.setFormatter(fmt)
            log_stream_handler.setLevel(self.__level)
            self.__logger.addHandler(log_stream_handler)

        def __create_log_file_handler():
            #  文件输出设置
            log_file_handler = handlers.RotatingFileHandler(path, backupCount=log_max_file_size,
                                                            maxBytes=log_max_file_num)
            log_file_handler.setFormatter(fmt)
            log_file_handler.setLevel(self.__level)
            self.__logger.addHandler(log_file_handler)

        #  输出类型判断
        if log_out_type.lower() == 'all':
            __create_log_stream_handler()
            __create_log_file_handler()
        elif log_out_type.lower() == 'file':
            __create_log_file_handler()
        elif log_out_type.lower() == 'terminal':
            __create_log_stream_handler()
        else:
            print("logOutType的值有误")
            sys.exit(0)

    def debug(self, msg):
        self.__logger.debug(msg)

    def info(self, msg):
        self.__logger.info(msg)

    def warn(self, msg):
        self.__logger.warning(msg)

    def error(self, msg):
        self.__logger.error(msg)

    def critical(self, msg):
        self.__logger.critical(msg)


if __name__ == '__main__':
    logOutType = 'all'  # 日志输出类型有三种值，all表示把日志输出到日志文件和屏幕上，file表示只输出到日志文件，terminal表示只输出到命令行
    logPath = '\logs'
    logFileName = 'info.txt'  # 日志文件名
    logLevel = 'debug'  # 当前日志等级有5种，logLevel = 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'
    logMaxFileNum = 30  # 每个日志文件的最大字节数，单位为M，超过这个大小自动新生成一个日志文件
    logMaxFileSize = 10  # 最大的日志文件个数，超过这个值，最早的日志文件自动被删除

    logger = Logger(logPath, logFileName, logMaxFileSize, logMaxFileNum, logOutType, logLevel)
    logger.debug("debug")
    logger.info("info")
    logger.warn("warn")
    logger.error("error")
    logger.critical("critical")
