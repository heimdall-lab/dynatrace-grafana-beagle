from pandas.core import indexing
from pandas.core.frame import DataFrame
from app.core.DatetimeUtils import DatetimeUtils
from datetime import datetime
from os import walk
import pandas as pd
import os
from collections import deque
from pathlib import Path
from datetime import datetime, timedelta
from dateutil.parser import parse
from os import path
import json
import logging
import glob

class CSVGateway:

    def __init__(self, app_dir_output, app_dyn_tag):      
        self.app_dyn_tag = app_dyn_tag.replace(":", "_")          
        self.logger = logging.getLogger(__class__.__name__)
        self.current_output_dir = app_dir_output
        
        if not os.path.isdir(path.join(app_dir_output, "problems")):
            os.makedirs(path.join(app_dir_output, "problems"))

        self.current_problem_path = path.join(app_dir_output, f"{self.app_dyn_tag}.log")        
        self.current_problem_csv_path = path.join(app_dir_output, f"{self.app_dyn_tag}.csv")        
        self.current_problem_exception_path = path.join(app_dir_output, f"{self.app_dyn_tag}_exceptions.csv")        
    
    
    def get_problem_begin_anchor(self):
        if os.path.exists(self.current_problem_path):
            with open(self.current_problem_path, 'r') as f:                
                str = f.readlines()[0]
                d = json.loads(str)                
                temp = DatetimeUtils.convert_from_timestamp(d['startTime'])
                return datetime(temp.year, temp.month, temp.day)
        else:    
            return datetime.now()
    
    def get_problem_anchor(self):        
        if os.path.exists(self.current_problem_path):
            with open(self.current_problem_path, 'r') as f:                
                str = f.readlines()[-1]
                d = json.loads(str)                
                temp = DatetimeUtils.convert_from_timestamp(d['startTime'])
                return datetime(temp.year, temp.month, temp.day)
        else:    
            return datetime.now() - timedelta(days=90)
    
    
    def read_problems(self):                         
        if not os.path.exists(self.current_problem_path):            
            return []
        result = []
        with open(self.current_problem_path, 'r') as f:
            for l in f.readlines():
                d = json.loads(l)
                result.append(d)
        return result
    
    def read_problems_csv(self):                           
        if not os.path.exists(self.current_problem_csv_path):            
            return None
        
        df = pd.read_csv(self.current_problem_csv_path, parse_dates=['start','end', 'event_start', 'event_end'])        
        return df

    def create_problem_entry(self, model):
        with open(self.current_problem_path, 'a') as f:
            line = json.dumps(model)                     
            f.write(line + "\n")      

   