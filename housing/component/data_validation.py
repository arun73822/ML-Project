from housing.logger import logging
from housing.exception import Housing_Exception
from housing.entity.config_entity import Data_Validation_Config
from housing.constants import *
from housing.entity.artifact_entity import Data_Validation_Artifact,Data_Ingestion_Artifact
from housing.config.configuration import Configuration
from housing.util.util import read_yaml_file
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import pandas as pd
import json
import os,sys

class Data_Validation:

    def __init__(self,data_validation_config : Data_Validation_Config,
                 data_ingestion_artifact : Data_Ingestion_Artifact):
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def is_train_test_file_exits(self)-> bool:
        try:

            is_train_file_exits= False
            is_test_file_exits= False

            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            is_train_file_exits= os.path.exists(train_file_path)
            is_test_file_exits= os.path.exists(test_file_path)

            is_available= is_train_file_exits and is_test_file_exits
            logging.info(f"Is train and test file exists?-> {is_available}")

            if not is_available:
                training_file=self.data_ingestion_artifact.train_file_path
                testing_file=self.data_ingestion_artifact.test_file_path
                message=f"Training file: {training_file} or Testing file: {testing_file} is not present"
                raise Exception(message)

            return is_available
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def get_train_test_df(self)-> pd.DataFrame:
        try:
            train_file= pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_file= pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_file,test_file
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def validate_dataset_schema(self)->bool:
        try:
            validation_status= False

            # checking the Number columns
            train_file_path=self.data_ingestion_artifact.train_file_path
            housing_dataframe=pd.read_csv(train_file_path)
            housng_dataframe_columns=list(housing_dataframe.columns)
            schema_info=read_yaml_file(file_path=self.data_validation_config.schema_file_path)
            schema_column_names=list(schema_info['columns'].keys())

            if len(housng_dataframe_columns) == len(schema_column_names):
                Number_of_columns= True
            
            if Number_of_columns == False:
                message= f"""housing data frame columns are {len(housng_dataframe_columns)} is not equal to
                             in schema file available columns are {len(schema_column_names)}"""
                raise Exception(message)

            # Check the columns names
            if housng_dataframe_columns == schema_column_names:
                Columns_names= True
            
            if Columns_names == False:
                message= f"""housing data frame columns are {(housng_dataframe_columns)} is not equal to
                             in schema file available columns are {(schema_column_names)}"""
                raise Exception(message)

            # Check the values of ocean proximity
            housing_dataframe_ocean_proximity=list(housing_dataframe['ocean_proximity'].value_counts().index)
            schema_ocean_proximity_list=list(schema_info['domain_value'].values())
        
            if housing_dataframe_ocean_proximity == schema_ocean_proximity_list[0]:
                Ocean_proximity= True
            
            if Ocean_proximity == False:
                message= f"""housing data frame columns are {(housing_dataframe_ocean_proximity)} is not equal to
                             in schema file available columns are {(schema_ocean_proximity_list)}"""
                raise Exception(message)

            validation_status= Number_of_columns and Columns_names and Ocean_proximity
            logging.info(f"Schema file validation is ?-> {validation_status}")
            return validation_status

        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def get_and_save_data_drift_report(self):
        try:
            profile=Profile(sections=[DataDriftProfileSection()])
            train_df,test_df=self.get_train_test_df()
            profile.calculate(train_df,test_df)

            report=json.loads(profile.json())

            report_file_path= self.data_validation_config.report_file_path
            report_file_dir= os.path.dirname(report_file_path)
            os.makedirs(report_file_dir,exist_ok=True)

            with open(report_file_path,'w') as report_file:
                json.dump(report,report_file,indent=6)
                return report
        except Exception as e:
            raise Housing_Exception(e,sys) from e
    
    def get_and_save_data_drift_report_page(self):
        try:
            dashboard=Dashboard(tabs=[DataDriftTab()])
            train_df,test_df=self.get_train_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path=self.data_validation_config.report_page_file_path
            report_page_file_dir= os.path.dirname(report_page_file_path)

            os.makedirs(report_page_file_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def data_drift_found(self)-> bool:
        try:

            report=self.get_and_save_data_drift_report()
            self.get_and_save_data_drift_report_page()
            return True
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def initiate_data_validation(self)-> Data_Validation_Artifact:
        try:

            self.is_train_test_file_exits()
            self.get_train_test_df()
            self.data_drift_found()
            self.validate_dataset_schema()

            data_validation_artifact=Data_Validation_Artifact(schema_file_path=self.data_validation_config.schema_file_path,
                                                            report_file_path=self.data_validation_config.report_file_path,
                                                            report_page_file_path=self.data_validation_config.report_page_file_path,
                                                            is_validated= True,message="Data Validation performed successully.")
            
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def __del__(self):
        logging.info(f"{'='*20}Data Valdaition log completed.{'='*20} \n\n")
        