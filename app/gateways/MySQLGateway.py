from datetime import datetime, timedelta
from typing import List
import pandas as pd
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine, text
from app.core.BaseEntity import Base
from sqlalchemy.orm import sessionmaker
from app.core.ProblemItemEntity import ProblemItemEntity
from app.core.DailyProblemItemEntity import DailyProblemItemEntity

class MySQLGateway:
    def __init__(self, username, password, server, port, database) -> None:
        self.connection = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(username, password, server, port, database)
        self.server = server
        self.username = username
        self.password = password
        self.port = port
        self.database = database
        self.engine = create_engine(self.connection)
        self.sessionmaker = sessionmaker(bind = self.engine)    

    def to_sql(self, table_name, df: pd.DataFrame):
        engine = create_engine(self.connection, echo=False)
        df.to_sql(name=table_name, con=engine, if_exists = 'replace')
    
    
    def create_database(self):
        Base.metadata.create_all(self.engine)
            
            
    def get_problems_by_ratio(self, ratio, period):
         with self.engine.connect() as con:
            rs = con.execute(text(
        """        
            select event_name as source, start, event_start, problem
            from daily_problems
            where start >= :anchor and TIMESTAMPDIFF(MINUTE, start, event_start) <= :ratio
            order by problem
        """), { 'ratio' : ratio, 'anchor': datetime.now() - timedelta(days=period) })
            result = list()
            for r in rs:
                result.append({
                    'source': r[0],
                    'start': r[1],
                    'event_start': r[2],
                    'problem': r[3]
                })
                
            return result
            
    
    def get_min_start(self):
        session = self.sessionmaker()
        min_start = session.scalar("select min(start) from problems")
        min_ids = list()
        with self.engine.connect() as con:
            rs = con.execute(
        """        
            select distinct problem 
            from problems
            where start  = (select start from problems order by start asc limit 1)
        """)
            for row in rs:
                min_ids.append(row[0])
                
        if not min_ids:
            return datetime.now(), min_ids
        
        return min_start, min_ids
     
    def send_problem_item(self, item):
        session = self.sessionmaker()
        session.add(item)
        session.commit()

    def send_problem_items(self, items: List):
        session = self.sessionmaker()
        if not  items:
            return
        for i in items:
            self.session.add(i)
        session.commit()
    
    def to_sql(self, table_name, df: pd.DataFrame):
        df.to_sql(name=table_name, con=self.engine, if_exists = 'replace')
        
    