from housing.logger import logging
from housing.exception import Housing_Exception
from housing.entity.config_entity import Data_Ingestion_Config
from housing.entity.artifact_entity import Data_Ingestion_Artifact
from housing.config.configuration import Configuration
from housing.component.data_ingestion import Data_Ingestion
import os,sys

class Pipeline:
    def __init__(self,config:Configuration=Configuration()):
        try:
           self.config=config
        except Exception as e:
            raise Housing_Exception(e,sys) from e
    
    def start_data_ingestion(self)->Data_Ingestion_Artifact:
        try:
            data_ingestion=Data_Ingestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.iniate_data_ingestion()
        except Exception as e:
            raise Housing_Exception(e,sys) from e
    def start_data_validation(self):
        pass

    def start_data_transformation(self):
        pass

    def start_model_trainer(self):
        pass

    def start_model_evaluation(self):
        pass

    def start_model_pusher(self):
        pass

    def run_pipeline(self):
        try:
            #data ingestion
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise Housing_Exception(e,sys) from e