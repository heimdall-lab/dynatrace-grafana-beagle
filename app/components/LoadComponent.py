from typing import List
from charset_normalizer import logging
import pandas as pd
from app.core.DailyProblemItemEntity import DailyProblemItemEntity
from app.core.DatetimeUtils import DatetimeUtils
from app.core.ProblemCollection import ProblemCollection
from app.core.ProblemItemEntity import ProblemItemEntity

from app.gateways.CSVGateway import CSVGateway
from app.gateways.DynatraceGateway import DynatraceGateway
from app.gateways.MySQLGateway import MySQLGateway
from app.core.DataframeUtil import DataframeUtil
from datetime import datetime, timedelta

class LoadComponent: 
        
    def __init__(self, mysql_gateway : MySQLGateway, 
                 csv_gateway: CSVGateway, 
                 dynatrace_gateway: DynatraceGateway, 
                 current_datetime: datetime,
                 entity_tag: str, 
                 app_batch: int,
                 start_day: int,
                 end_day: int) -> None:
        self.logger = logging.getLogger(__class__.__name__)
        self.mysql_gateway = mysql_gateway
        self.csv_gateway = csv_gateway        
        self.dynatrace_gateway = dynatrace_gateway
        self.current_datetime = current_datetime
        self.entity_tag = entity_tag
        self.app_batch = app_batch
        self.start_day = int(start_day)
        self.end_day = int(end_day)
        
    def prepare(self):
        self.logger.warning('setup database')
        self.mysql_gateway.create_database()
        
        
    def load_online(self):
        start_on = self.csv_gateway.get_problem_anchor()        
        limit = datetime(self.current_datetime.year, self.current_datetime.month, self.current_datetime.day)
        count  = 0
        while start_on < limit:        
            next_date = start_on + timedelta(hours=23, minutes=59, seconds=59)        
            self.logger.info("problem sync {} sli between {} - {}".format(self.entity_tag, start_on, next_date))            
            self.__load_dynatrace_data(start_on, next_date)
            start_on = next_date + timedelta(seconds=1)       
            count += 1
            if count >= self.app_batch:
                break
            

    def __load_dynatrace_data(self, start: datetime, end: datetime):
        problems = self.dynatrace_gateway.get_problems(start, end)
        items = sorted(problems["result"]["problems"], 
                       key=lambda x: DatetimeUtils.convert_from_timestamp(int( x['endTime']) ))
        for item in items:
            problems_ds = self.dynatrace_gateway.get_problem(item['id'])['result']            
            self.csv_gateway.create_problem_entry(problems_ds)
            collection = ProblemCollection(problems_ds, self.entity_tag)
            result = collection.parse()
            self.__send_database(result)
   
    def __send_database(self, items: List[ProblemItemEntity]):
        
        if not items:
            return
        
        self.logger.warning('sync log database sync problem: {} {}'.format( items[0].display_name, len(items) ))
        
        self.mysql_gateway.send_problem_items(items)

        daily_problems_filtered = filter(lambda x: x.start.hour >= self.start_day and x.end.hour <= self.end_day, items)
        
        daily_problems = list(map( lambda x: DailyProblemItemEntity(x), daily_problems_filtered))
        
        self.logger.warning('sync log database sync daily problem: {}'.format( len(daily_problems) ))
     
        self.mysql_gateway.send_problem_items(daily_problems)
   
    def load_log(self):
        self.logger.warning("start sync log")
        min_start , min_ids  = self.mysql_gateway.get_min_start()
        problems = self.csv_gateway.read_problems()
        self.logger.warning("sync {} logs".format(len(problems))) 
        for item in problems:
            collection = ProblemCollection(item, self.entity_tag)
            result = collection.parse()
            temp = list()
            for r in result:
                if r.start <= min_start and r.problem not in min_ids:
                    temp.append(r)
            self.__send_database(temp)
            
        # working_problems = problems[(problems['start'].dt.hour > 5) & (problems['start'].dt.hour < 22)]
        # severity = DataframeUtil.prepare_export(problems['severity'])
        # impact = DataframeUtil.prepare_export(problems['impact'])
        # event_impact = DataframeUtil.prepare_export(problems['event_impact'])
        # event_severity = DataframeUtil.prepare_export(problems['event_severity'])
        # event_names = DataframeUtil.prepare_export(problems['event_name'])
        # display_names = DataframeUtil.prepare_export(problems['display_name'])
        # event_type = DataframeUtil.prepare_export(problems['event_type'])
        # self.mysql_gateway.to_sql('event_type', event_type)
        # self.mysql_gateway.to_sql('severity', severity)
        # self.mysql_gateway.to_sql('impact', impact)
        # self.mysql_gateway.to_sql('event_impact', event_impact)
        # self.mysql_gateway.to_sql('event_severity', event_severity)
        # self.mysql_gateway.to_sql('event_names', event_names)
        # self.mysql_gateway.to_sql('problem_names', display_names)
        # self.mysql_gateway.to_sql('problems', problems)
        # self.mysql_gateway.to_sql('working_problems', working_problems)
        
        
               
        
    
    