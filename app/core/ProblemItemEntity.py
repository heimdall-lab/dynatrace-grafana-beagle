from tokenize import Double
from sqlalchemy import Column, DateTime, Integer, String, Float, BigInteger, Text, Boolean
from app.core.BaseEntity import Base

class ProblemItemEntity(Base):
    
    __tablename__ = 'problems'
    
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
    
    def __init__(self, problem, display_name, prefix, start, end, severity, impact, duration,
                 event_impact, event_severity, event_name, event_type, event_start, event_end,
                 root, event_duration, event_request_minute, event_service, event_group, event_method,
                 event_total_request) -> None:
        super().__init__()
        self.problem = problem
        self.display_name = display_name
        self.prefix = prefix
        self.start = start
        self.end = end
        self.severity = severity
        self.impact = impact
        self.duration = duration
        self.event_impact = event_impact
        self.event_severity = event_severity
        self.event_name = event_name
        self.event_type = event_type
        self.event_start = event_start
        self.event_end = event_end
        self.root = root
        self.event_duration = event_duration
        self.event_request_minute  = event_request_minute
        self.event_service = event_service
        self.event_group = event_group
        self.event_method = event_method
        self.event_total_request = event_total_request