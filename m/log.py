import logging
from logging.handlers import RotatingFileHandler
import sys
import time
from datetime import datetime

class Log(object):
    def __init__(self) :

        logging.addLevelName(25, "SUCCESS")
        logging.addLevelName(45, "ILLEGALUSER")

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-15s :: %(levelname)s :: %(message)s')

        file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        file_handler_error = RotatingFileHandler('error.log', 'a', 1000000, 1)
        file_handler_error.setLevel(logging.ERROR)
        file_handler_error.setFormatter(formatter)
        self.logger.addHandler(file_handler_error)

        file_handler = RotatingFileHandler('illegal.log', 'a', 1000000, 1)
        file_handler.setLevel(logging.ILLEGALUSER)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(logging.NOTSET)
        self.logger.addHandler(steam_handler)


    def printL(self,pMsg,pLvl):
        if pLvl == 10 :
            pMsg = bcolors.DEBUG + pMsg + bcolors.ENDC
        elif pLvl == 20 :
            pMsg = bcolors.INFO + pMsg + bcolors.ENDC
        elif pLvl == 25 :
            pMsg = bcolors.SUCCESS + pMsg + bcolors.ENDC
        elif pLvl == 30 :
            pMsg = bcolors.WARNING + pMsg + bcolors.ENDC
        elif pLvl == 40 or pLvl ==45 :
            pMsg = bcolors.FAIL + pMsg + bcolors.ENDC
        self.logger.log(pLvl,pMsg)


class bcolors:
    DEBUG = '\033[94m'
    INFO = '\033[95m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'




