from datetime import datetime
import os
import unittest
from app.components.LoadComponent import LoadComponent
from app.gateways.CSVGateway import CSVGateway
from app.gateways.DynatraceGateway import DynatraceGateway
from app.gateways.MySQLGateway import MySQLGateway

class TestSyncService(unittest.TestCase):
    
    def test_sync(self):
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
        component = LoadComponent(mysql, csv, dynatrace, datetime.now(), tag_service, 1)
        component.prepare()
        component.load_online()    
    
    def test_sync_log(self):
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
                                  os.environ['app__start_day'], os.environ['app__end_day'])
        component.prepare()
        component.load_log()    
        
        
        