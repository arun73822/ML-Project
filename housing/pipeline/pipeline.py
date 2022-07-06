from housing.component.data_transformation import Data_Transformation
from housing.exception import Housing_Exception
from housing.entity.config_entity import Data_Ingestion_Config,Data_Validation_Config
from housing.entity.artifact_entity import Data_Ingestion_Artifact, Data_Transformation_Artifact,Data_Validation_Artifact
from housing.config.configuration import Configuration
from housing.component.data_ingestion import Data_Ingestion
from housing.component.data_validation import Data_Validation
import os,sys

class Pipeline:
    def __init__(self,config: Configuration = Configuration())-> None:
        try:
           self.config=config
        except Exception as e:
            raise Housing_Exception(e,sys) from e
    
    def start_data_ingestion(self)->Data_Ingestion_Artifact:
        try:
            data_ingestion=Data_Ingestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def start_data_validation(self,data_ingestion_artifact:Data_Ingestion_Artifact)->Data_Validation_Artifact:

        try:
            data_validation=Data_Validation(data_validation_config=self.config.get_data_validation_config(),
                                            data_ingestion_artifact=data_ingestion_artifact)

            return data_validation.initiate_data_validation()
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def start_data_transformation(self,data_ingestion_artifact:Data_Ingestion_Artifact,
                        data_validation_artifact:Data_Validation_Artifact)->Data_Transformation_Artifact:
        try:
            data_transformation = Data_Transformation(
                data_transformation_config=self.config.get_data_transformation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validaton_artifact=data_validation_artifact)
                
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def run_pipeline(self):
        try:
            # data_ingestion
            data_ingestion_artifact= self.start_data_ingestion()

            # data_validation
            data_validation_artifact= self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact)
            
            # data_transformation
            data_tranformation_artifact=self.start_data_transformation(
                          data_ingestion_artifact=data_ingestion_artifact,
                          data_validation_artifact=data_validation_artifact)

        except Exception as e:
            raise Housing_Exception(e,sys) from e
            