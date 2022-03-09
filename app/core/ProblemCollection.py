from datetime import datetime
import json
from operator import is_not
from typing import List
from app.core.DatetimeUtils import DatetimeUtils
from app.core.ProblemItemEntity import ProblemItemEntity

class ProblemCollection:

    def __init__(self, data, prefix) -> None:
        self.data = data
        self.prefix = prefix
        
    def parse(self) -> List[ProblemItemEntity]:
        result = list()
        item = self.data
        start_time = DatetimeUtils.convert_from_timestamp(item['startTime'])
        end_time = DatetimeUtils.convert_from_timestamp(item['endTime'])
        duration = (end_time - start_time).seconds / (60)                        
        impacts = len(item['rankedEvents'])
        
        check = dict() # validate duplicates 
         
        for sub in item['rankedEvents']:
            
            if (item['id'], sub['entityId'], sub['entityName'], sub['eventType']) in check:
                continue
            
            sub['start_time'] = DatetimeUtils.convert_from_timestamp(sub['startTime'])
            sub['end_time'] = DatetimeUtils.convert_from_timestamp(sub['endTime'])
            duration_event = (sub['end_time'] - sub['start_time']).seconds / (60)            
            is_root = sub['isRootCause']
            
            problem = ProblemItemEntity(item['id'], item['displayName'], self.prefix, start_time, end_time
                                        , item['severityLevel'], item['impactLevel'], duration,
                                        sub['impactLevel'],
                                        sub['severityLevel'],
                                        sub['entityName'],
                                        sub['eventType'],
                                        sub['start_time'],
                                        sub['end_time'],
                                        is_root, 
                                        duration_event,
                                        sub.get('affectedRequestsPerMinute', 0),
                                        sub.get('service', None),
                                        sub.get('serviceMethodGroup', None),
                                        sub.get('serviceMethod', None),
                                        sub.get('affectedRequestsPerMinute', 0) * duration_event
                                        )
            
            result.append(problem)
        
        return result
                