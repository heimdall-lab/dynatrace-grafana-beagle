from tokenize import Double
from sqlalchemy import Column, DateTime, Integer, String, Float, BigInteger, Text, Boolean
from app.core.BaseEntity import Base
from app.core.ProblemItemEntity import ProblemItemEntity

class DailyProblemItemEntity(Base):
    
    __tablename__ = 'daily_problems'
    id = Column(BigInteger, autoincrement=True, primary_key=True)    
    problem = Column(String(256), nullable=False)
    display_name = Column(String(256), nullable=False)
    prefix = Column(String(256), nullable=False)
    start =  Column(DateTime, nullable=False)
    end =  Column(DateTime, nullable=False)
    severity =  Column(String(256), nullable=False)
    impact =  Column(String(256), nullable=False)
    duration =  Column(BigInteger, nullable=False)
    event_impact =  Column(String(256), nullable=False)
    #status =  Column(String(256), nullable=False)
    event_severity =  Column(String(256), nullable=False)
    event_name =  Column(String(2048), nullable=True)
    event_type =  Column(String(256), nullable=True)
    event_start =  Column(DateTime, nullable=False)
    event_end =  Column(DateTime, nullable=False)
    root =  Column(Boolean, nullable=False)
    event_duration =  Column(Float, nullable=True)
    event_request_minute =  Column(Float, nullable=True)
    event_service =  Column(String(512), nullable=True)
    event_group =  Column(String(512), nullable=True)
    event_method =  Column(Text, nullable=True)
    # impacts =  Column(Integer, nullable=False)
    event_total_request =  Column(Integer, nullable=False)
    # source =  Column(String(1024), nullable=False)
    # tbf =  Column(Integer, nullable=False)
    # blast =  Column(Integer, nullable=False)
    
    def __init__(self, item: ProblemItemEntity) -> None:
        super().__init__()
        self.problem = item.problem
        self.display_name = item.display_name
        self.prefix = item.prefix
        self.start = item.start
        self.end = item.end
        self.severity = item.severity
        self.impact = item.impact
        self.duration = item.duration
        self.event_impact = item.event_impact
        self.event_severity = item.event_severity
        self.event_name = item.event_name
        self.event_type = item.event_type
        self.event_start = item.event_start
        self.event_end = item.event_end
        self.root = item.root
        self.event_duration = item.event_duration
        self.event_request_minute  = item.event_request_minute
        self.event_service = item.event_service
        self.event_group = item.event_group
        self.event_method = item.event_method
        self.event_total_request = item.event_total_request