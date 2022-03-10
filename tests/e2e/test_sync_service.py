from datetime import datetime
import os
import unittest
from app.components.LoadComponent import LoadComponent
from app.gateways.CSVGateway import CSVGateway
from app.gateways.DynatraceGateway import DynatraceGateway
from app.gateways.MySQLGateway import MySQLGateway

class TestSyncService(unittest.TestCase):
    
    def setUp(self):
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
        self.component = LoadComponent(mysql, csv, dynatrace, datetime.now(), tag_service, 1, 
                                       os.environ['app__start_day'], 
                                       os.environ['app__end_day'],
                                       os.environ['app__analysis_days'],
                                       os.environ['app__analysis_minsup'], 
                                       os.environ['app__analysis_confidence'],
                                       os.environ['app__blast_ratio'] 
                                       )
        
    
    def test_association_mining(self):
        self.component.prepare()
        self.component.load_association()
    
    def test_sync(self):
        self.component.prepare()
        self.component.load_online()    
    
    def test_sync_log(self):
        self.component.prepare()
        self.component.load_log()    
        
        
        