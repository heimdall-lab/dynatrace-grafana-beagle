from datetime import datetime
import os
import unittest
from app.components.LoadComponent import LoadComponent
from app.gateways.CSVGateway import CSVGateway
from app.gateways.DynatraceGateway import DynatraceGateway
from app.gateways.MySQLGateway import MySQLGateway
from dotenv import load_dotenv
import logging
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.WARNING)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(filename)s] [%(lineno)s] %(message)s")

rootLogger = logging.getLogger()
rootLogger.removeHandler(logging.getLogger().handlers[0])

fileHandler = logging.FileHandler("app.log")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

logger = logging.getLogger()   

if __name__ == "__main__":
    load_dotenv()
    mysql = MySQLGateway(
        os.environ['mysql__username'],
        os.environ['mysql__password'],
        os.environ['mysql__server'],
        os.environ['mysql__port'],
        os.environ['mysql__database'])
    tag_service = os.environ['app__tag_service']
    csv = CSVGateway('wip', tag_service)
    dynatrace = DynatraceGateway( 
            os.environ['app__dyn_host'],
            os.environ['app__dyn_token'],
            os.environ['app__tag_service']
    )
    component = LoadComponent(mysql, csv, dynatrace, datetime.now(), tag_service, 1,
                                os.environ['app__start_day'], os.environ['app__end_day'],
                                os.environ['app__analysis_days'], os.environ['app__analysis_minsup'],
                                os.environ['app__analysis_confidence'], 
                                os.environ['app__blast_ratio'])
    component.prepare()
    component.load_log()   