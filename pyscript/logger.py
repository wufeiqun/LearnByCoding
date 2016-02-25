#coding=utf-8
import os
import sys
import logging
import logging.handlers

LOG_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + '/log/'
LOG_NAME = 'qfmonitor.log'

def initlog():
    #初始化logger,日志级别设置的最低,保证所有级别的日志都可以进入下一个环节,过滤操作在下一个步骤handler来过滤.
    logger = logging.getLogger('root')
    logger.setLevel(logging.DEBUG)
    #create the handler(console and file)
    myFileHandler = logging.handlers.TimedRotatingFileHandler(filename=LOG_DIR+LOG_NAME, when='midnight', interval=1, backupCount=30, encoding='utf-8')
    myFileHandler.setLevel(logging.INFO)
    myStreamHandler = logging.StreamHandler()
    myStreamHandler.setLevel(logging.DEBUG)
    #create the formatter
    fmt = logging.Formatter('%(asctime)s:%(lineno)s:%(levelname)s:%(message)s')
    myFileHandler.setFormatter(fmt)
    myStreamHandler.setFormatter(fmt)
    #add the handler to logger
    logger.addHandler(myFileHandler)
    logger.addHandler(myStreamHandler)

    return logger

