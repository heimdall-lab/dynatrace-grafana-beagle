import urllib3
from app.components.LoadComponent import LoadComponent
from app.gateways.CSVGateway import CSVGateway
from app.gateways.DynatraceGateway import DynatraceGateway
from app.gateways.MySQLGateway import MySQLGateway
import logging
from flask import Flask
from flask_apscheduler import APScheduler
import os
from datetime import datetime

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


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

# create app
app = Flask(__name__)
app.config.from_object(Config())

# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)


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
                                       os.environ['app__start_day'], 
                                       os.environ['app__end_day'],
                                       os.environ['app__analysis_days'],
                                       os.environ['app__analysis_minsup'], 
                                       os.environ['app__analysis_confidence'],
                                       os.environ['app__blast_ratio'] )


@scheduler.task('interval', id='monitoring_job', seconds=5)
def monitoring_job():
    logger.warning('running at {}'.format(datetime.now()))
    
        
@scheduler.task('interval', id='do_sync', seconds=60, misfire_grace_time=900, max_instances=1)
def sync_job():
    try:
        component.load_online()    
    except Exception as ex:
        logger.exception(ex)

@scheduler.task('interval', id='do_sync_log', seconds=300, misfire_grace_time=900, max_instances=1)
def do_sync_log():
    try:
        component.load_log()    
    except Exception as ex:
        logger.exception(ex)

@scheduler.task('interval', id='do_sync_analisys', seconds=120, misfire_grace_time=900, max_instances=1)
def do_sync_analisys():
    try:
        component.load_association()    
    except Exception as ex:
        logger.exception(ex)


if __name__ == "__main__":
    logger.warning('start agent at {}'.format(datetime.now()))
    scheduler.start()
    component.prepare()
    app.run()