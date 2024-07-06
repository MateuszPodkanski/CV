import os
import glob
import pandas as pd

class File:
    
    def __init__(self,folder_path):
        self.folder_path = folder_path
        self.excel_file = self.find_excel_file()
    
    def find_excel_file(self):
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith('.csv'):
                return os.path.join(self.folder_path, file_name)
        raise Exception ("There are no files in picked folder")
    
class DataFrame:

    def __init__(self,excel_file):
        self.excel_file = excel_file
        self.df = self.prepare_dataframe()

    def prepare_dataframe(self):
        df = pd.read_csv(self.excel_file,skiprows=6)

        if df.shape[1] != 12:
            raise Exception(f"Excel is containing {df.shape[1]} columns instead of 12")
        return df
    
    def extract_first_dot(self,value):
        parts = value.split('.',1)
        return parts[1] 
    
    def extract_ASIN_part(self,value):
        if 'B0' in value:
            part = value.split('B0')[1]
            ASIN = 'B0' + part[:8]
            return ASIN
        elif 'ASIN:' in value:
            part = value.split('ASIN:')[1]
            ASIN = part.split(',')[0]
            return ASIN
        else:
            return 'NO ASIN FOUND'
    
    # def extract_ASIN(self,value):
    #     parts = value.split(':')
    #     return parts[1]

    def extract_merchant_ID(self,value):
        if 'SELLER:' in value:
            part = value.split('SELLER:')[1]
            merchant = part.split(',')
            return merchant
        
        elif 'VENDOR:' in value :
            part = value.split('VENDOR:')[1]
            merchant = part.split(',')
            return merchant
        
        else:
            return 'NO MERCHANT FOUND'
    


    def new_column_basing_old(self,new_column_name : str,based_column_name : str,function):
        if "Subject" in self.df.columns:
            self.df[new_column_name] = self.df[based_column_name].apply(function)

    def new_column(self, new_column_name : str , string_to_add : str):
        self.df[new_column_name] = string_to_add

    def new_column_merged(self, new_column_name : str, column_1_name : str, column_2_name : str):
        self.df[new_column_name] = self.df[column_1_name].astype(str) + self.df[column_2_name].astype(str)

    def change_columns_order(self,columns):
        self.df = self.df[columns]
    
    def save_df(self):
        self.df.to_csv('prepared allocation.csv',index=False)

print('Work in progress do not close')    

file = File('C:\\New Folder')

df = DataFrame(file.excel_file)

df.new_column_basing_old('ASIN','Subject',df.extract_ASIN_part)

df.new_column_basing_old('marketplace','Queue',df.extract_first_dot)

df.new_column('general link', 'https://paragon-eu.amazon.com/hz/view-case?caseId=')

df.new_column('break',' ')

df.new_column_merged('case link','general link','ID')

desired_order =['Last Inbound Date','ID','case link','Partner','Owner','Status','ASIN','Last Outbound Date','Creation Date','marketplace']

df.change_columns_order(desired_order)

df.save_df()

print('Success, new file generated!')


