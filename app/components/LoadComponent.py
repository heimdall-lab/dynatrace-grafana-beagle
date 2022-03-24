import sys
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
from mlxtend.frequent_patterns import apriori, association_rules, fpmax, fpgrowth
from mlxtend.preprocessing import TransactionEncoder
from itertools import groupby
import numpy as np
class LoadComponent: 
        
    def __init__(self, mysql_gateway : MySQLGateway, 
                 csv_gateway: CSVGateway, 
                 dynatrace_gateway: DynatraceGateway, 
                 current_datetime: datetime,
                 entity_tag: str, 
                 app_batch: int,
                 start_day: int,
                 end_day: int, 
                 analysis_days: int,
                 analysis_minsup: float,
                 analysis_confidence: float,
                 blast_ratio: int) -> None:
        self.blast_ratio = int(blast_ratio)
        self.analysis_minsup = float(analysis_minsup)
        self.analysis_confidence = float(analysis_confidence)
        self.analysis_days = int(analysis_days)
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
        
        

        daily_problems_filtered = filter(lambda x: x.start.hour >= self.start_day and x.end.hour <= self.end_day, items)
        
        daily_problems = list(map( lambda x: DailyProblemItemEntity(x), daily_problems_filtered))
        
        self.logger.warning('sync log database sync daily problem: {}'.format( len(daily_problems) ))
     
        self.mysql_gateway.send_problem_items(items)
        
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
            
    def load_association(self):
        self.logger.warning("start association mining")
        items = self.mysql_gateway.get_problems_by_ratio(self.blast_ratio, self.analysis_days)
        itemsets = list()
        if items:
            for k, g in groupby(items, key=lambda x:x['problem']):
                group = sorted(g, key=lambda x: x['event_start'])
                itemsets.append( [ x['source'] for x in group ])
                
            te = TransactionEncoder()
            a_data = te.fit(itemsets).transform(itemsets)
            ml_temp = pd.DataFrame(a_data, columns=te.columns_)
            ml_res = apriori(ml_temp, min_support = self.analysis_minsup, use_colnames = True, verbose = 1)
            ml_res['length'] = ml_res['itemsets'].apply(lambda x: len(x))
         
            result = association_rules(ml_res, metric="confidence", min_threshold=self.analysis_confidence)
            result.replace([np.inf], sys.maxsize, inplace=True)
            result.replace([-np.inf], -1 * sys.maxsize, inplace=True)
            result["antecedents"] = result["antecedents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
            result["consequents"] = result["consequents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
            self.mysql_gateway.to_sql('daily_problems_associations', result)
 
        
        
               
        
    
    