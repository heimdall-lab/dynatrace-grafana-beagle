import requests

from app.core.DatetimeUtils import DatetimeUtils 


class DynatraceGateway:
    
    def __init__(self, dynatrace_host, dynatrace_token, dynatrace_tag_service):        
        self.token = "Api-Token {}".format(dynatrace_token)
        self.host = dynatrace_host
        self.service_tag = dynatrace_tag_service        

    def get_problems(self, start, end):
        start_stamp = DatetimeUtils.convert_to_timestamp(start)
        end_stamp = DatetimeUtils.convert_to_timestamp(end)        
        target_url = self.host + "problem/feed?tag={}&status=CLOSED&startTimestamp={}&endTimestamp={}".format(
            self.service_tag, start_stamp, end_stamp)
        response = requests.get(target_url,  
                                headers={"Authorization": self.token, "accept": "application/json"},
                                verify=False)

        if response.status_code > 299:
            raise ValueError(response.status_code)

        return response.json()
    
    def get_problem(self, id):        
        target_url = self.host + "problem/details/{}".format(id)
        response = requests.get(target_url,  
                                headers={"Authorization": self.token, "accept": "application/json"},
                                verify=False)
        
        if response.status_code > 299:
            raise ValueError(response.status_code)

        return response.json()

    
    
    
    
    
    
    
    