from housing.constants import ROOT_DIR
from housing.logger import logging
from housing.exception import Housing_Exception
from housing.entity.config_entity import (Data_Ingestion_Config,Data_Transformation_Config,
                                          Data_Validation_Config,Model_Evaluation_Config,Model_Pusher_Config,
                                          Model_Trainer_Config,Training_Pipeline_Config)
from housing.entity.artifact_entity import Data_Ingestion_Artifact
from housing.config.configuration import Configuration
from housing.constants import *
from six.moves import urllib
from sklearn.model_selection import StratifiedShuffleSplit
import sys,os
import tarfile
import pandas as pd
import numpy as np

class Data_Ingestion:
    def __init__(self,data_ingestion_config:Data_Ingestion_Config):
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20} ")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise Housing_Exception(e,sys)
    
    def download_housing_data(self)-> str:
        try:
            download_ulr=self.data_ingestion_config.dataset_download_url

            tgz_download_dir=self.data_ingestion_config.tgz_data_dir

            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)
            
            os.makedirs(tgz_download_dir,exist_ok=True)

            housing_file_name= os.path.basename(download_ulr)

            tgz_file_path= os.path.join(tgz_download_dir,housing_file_name)
            logging.info(f"Downloading file from :[{download_ulr}] into :[{tgz_file_path}]")
            urllib.request.urlretrieve(download_ulr,tgz_file_path)
            logging.info(f"File :[{tgz_file_path}] has been downloaded successfully.")
            return tgz_file_path

        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def extract_housing_data(self,tgz_file_path:str)-> str:
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)

            logging.info(f"Extracting tgz file: [{tgz_file_path}] into dir: [{raw_data_dir}]")

            with tarfile.open(raw_data_dir) as housing_file_obj:
                housing_file_obj.extractall(path=raw_data_dir)
                logging.info(f"Extraction completed")
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def split_data_as_train_test(self)->Data_Ingestion_Artifact:
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir

            housing_file_name=os.listdir(raw_data_dir)[0]
            housing_file_path= os.path.join(raw_data_dir,housing_file_name)
            logging.info(f"Reading csv file: [{housing_file_path}]")

            housing_data_frame=pd.read_csv(housing_file_path)

            housing_data_frame["income_cat"] = pd.cut(
                housing_data_frame["median_income"],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1,2,3,4,5])
        
            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None
            
            split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=45)

            for train_index,test_index in split.split(housing_data_frame,housing_data_frame["income_cat"]):
                strat_train_set = housing_data_frame.loc[train_index].drop(["income_cat"],axis=1)
                strat_test_set = housing_data_frame.loc[test_index].drop(["income_cat"],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            housing_file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        housing_file_name)
            
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_artifact = Data_Ingestion_Artifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def iniate_data_ingestion(self)-> Data_Ingestion_Artifact:
        try:
            tgz_file_path= self.download_housing_data()
            self.extract_housing_data(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise Housing_Exception(e,sys) from e
    
    def __del__(self):
        logging.info(f"{'='*20}Data Ingestion log completed.{'='*20} \n\n")