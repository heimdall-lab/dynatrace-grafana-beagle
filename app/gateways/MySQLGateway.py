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
        # db.Base.metadata.create_all(db.engine)
        # dbcon = self.__open_connection()
        # dbcur = dbcon.cursor()
        # dbcur.execute("""
        #     SELECT COUNT(*)
        #     FROM information_schema.tables
        #     WHERE table_name = 'problems'
        #     """)
        # exists = False
        # if dbcur.fetchone()[0] == 1:
        #     exists = True
        # dbcur.close()
        # if not exists:
        #     dbcur = dbcon.cursor()
        #     dbcur.execute("""
        #     CREATE TABLE `problems` (
        #     `index` bigint DEFAULT NULL,
        #     `id` text,
        #     `problem` text,
        #     `display_name` text,
        #     `prefix` double DEFAULT NULL,
        #     `start` datetime DEFAULT NULL,
        #     `end` datetime DEFAULT NULL,
        #     `severity` text,
        #     `impact` text,
        #     `duration` double DEFAULT NULL,
        #     `event_impact` text,
        #     `status` text,
        #     `event_severity` text,
        #     `event_id` text,
        #     `event_name` text,
        #     `event_type` text,
        #     `event_start` datetime DEFAULT NULL,
        #     `event_end` datetime DEFAULT NULL,
        #     `root` tinyint(1) DEFAULT NULL,
        #     `event_request_minute` double DEFAULT NULL,
        #     `event_service` text,
        #     `event_group` text,
        #     `event_method` text,
        #     `event_duration` double DEFAULT NULL,
        #     `impacts` bigint DEFAULT NULL,
        #     `event_total_request` double DEFAULT NULL,
        #     `source` text,
        #     `tbf` bigint DEFAULT NULL,
        #     `blast` bigint DEFAULT NULL,
        #     KEY `ix_problems_index` (`index`)
        #     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        #     """)
            
            
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
        
    def connect(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                            database='katarilab',
                                            user='root',
                                            password='test123', port=30306)
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                cursor.close()

            return connection

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            pass
            # if connection.is_connected():                
            #     connection.close()
            #     print("MySQL connection is closed")




