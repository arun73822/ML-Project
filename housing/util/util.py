from housing.exception import Housing_Exception
from housing.constants import *
import pandas as pd
import numpy as np
import os,sys
import yaml
import dill

def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns the contents as a dictionary.
    file_path: str
    """
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise Housing_Exception(e,sys) from e

def load_data(file_path:str,schema_file_path:str)->pd.DataFrame:
    try:
               schema_dataset=read_yaml_file(file_path=schema_file_path)

               schema_dataset_columns=schema_dataset[COLUMNS_OF_SCHEMA]
               data_frame=pd.read_csv(file_path)
               error_message=""
               for column in data_frame.columns:
                  if column in list(schema_dataset_columns.keys()):
                     data_frame[column].astype(schema_dataset_columns[column])
                  else:
                     error_message = f"{error_message} \nColumn: [{column}] is not in the schema."

               if len(error_message) > 0:
                  raise Exception(error_message)
               return data_frame
    except Exception as e:
        raise Housing_Exception(e,sys) from e

def save_numpy_array_data(file_path:str,array:np.array):
    try:
               dir_path=os.path.dirname(file_path)
               os.makedirs(dir_path,exist_ok=True)
               with open(file_path,"wb") as file_obj:
                  np.save(file_obj,array)
    except Exception as e:
        raise Housing_Exception(e,sys) from e   

def save_object(file_path:str,object):
            try:
               dir_path=os.path.dirname(file_path)
               os.makedirs(dir_path,exist_ok=True)
               with open(file_path,'wb') as file_obj:
                  dill.dump(object,file_obj)
            except Exception as e:
               raise Housing_Exception(e,sys) from e           