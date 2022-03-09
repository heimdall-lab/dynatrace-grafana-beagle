import pandas as pd


class DataframeUtil:
    
    @staticmethod
    def prepare_export( df: pd.DataFrame):        
        temp = df.drop_duplicates()
        #temp.set_index('index')        
        return temp
        