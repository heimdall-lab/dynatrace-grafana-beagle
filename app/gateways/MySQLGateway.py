from datetime import datetime
from typing import List
import pandas as pd
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
from app.core.BaseEntity import Base
from sqlalchemy.orm import Session
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
        self.session = Session(bind = self.engine)    

    def to_sql(self, table_name, df: pd.DataFrame):
        engine = create_engine(self.connection, echo=False)
        df.to_sql(name=table_name, con=engine, if_exists = 'replace')
    
    def __open_connection(self):
        temporal = mysql.connector.connect(host=self.server,
                                            database=self.database,
                                            user=self.username,
                                            password=self.password, port=self.port)
        return temporal
    
    def create_database(self):
        Base.metadata.create_all(self.engine)
            
    def get_min_start(self):
        min_start = self.session.scalar("select min(start) from problems")
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
        self.session.add(item)
        self.session.commit()

    def send_problem_items(self, items: List):
        if not  items:
            return
        for i in items:
            self.session.add(i)
        self.session.commit()
        
    