
from datetime import datetime

from helpers import logger

time1 = None


def start_time():
    global time1
    time1 = datetime.now()


def end_time(operation, enableLog=True):
    global time1
    diff_time = datetime.now() - time1
    logger.log("total time to "+str(operation)+": " + str(diff_time), enableLog)
