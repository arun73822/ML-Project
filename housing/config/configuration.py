from housing.logger import logging
from housing.exception import Housing_Exception
from housing.entity.config_entity import (Data_Ingestion_Config,Data_Validation_Config,
Data_Transformation_Config, Model_Evaluation_Config, Model_Pusher_Config, Model_Trainer_Config,Training_Pipeline_Config)
from housing.constants import *
from housing.util.util import read_yaml_file
import os,sys

class Configuration:
    def __init__(self,filepath:str=CONFIG_FILE_PATH,current_timestamp=CURRENT_TIME_STAMP)->None:
        try:
            self.config_info=read_yaml_file(file_path=filepath)
            self.training_pipeline_config=self.get_training_pipeline_config()
            self.current_timestamp=current_timestamp
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def get_data_ingestion_config(self)-> Data_Ingestion_Config:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir= os.path.join(artifact_dir,
                                                      DATA_INGESTION_ARTIFACT_DIR,
                                                      self.current_timestamp)

            data_ingestion_info=self.config_info[DATA_INGESTION_CONFIG_KEY]

            data_set_download_url=data_ingestion_info[DATA_INGESTION_DATASET_URL_KEY]

            raw_data_dir=os.path.join(data_ingestion_artifact_dir,
                                      data_ingestion_info[DATA_INGESTION_INGESTED_DIR])
            
            tgz_data_dir=os.path.join(data_ingestion_artifact_dir,
                                      data_ingestion_info[DATA_INGESTION_TGZ_DATA_DIR])

            ingested_data_dir= os.path.join(data_ingestion_artifact_dir,
                                            data_ingestion_info[DATA_INGESTION_INGESTED_DIR])

            ingested_train_dir= os.path.join(ingested_data_dir,
                                            data_ingestion_info[DATA_INGESTION_TRAIN_DATA_DIR])

            ingested_test_dir= os.path.join(ingested_data_dir,
                                            data_ingestion_info[DATA_INGESTION_TEST_DATA_DIR])

            data_ingestion_config=Data_Ingestion_Config(dataset_download_url=data_set_download_url,
                                                        raw_data_dir=raw_data_dir,
                                                        tgz_data_dir=tgz_data_dir,
                                                        ingested_train_dir=ingested_train_dir,
                                                        ingested_test_dir=ingested_test_dir)

            logging.info(f"Data Ingestion config: {data_ingestion_config}")                    
            return data_ingestion_config

        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def get_data_validation_config(self)-> Data_Validation_Config:
        try:
            schema_file_path= None
            data_validation_config=Data_Validation_Config(schema_file_path=schema_file_path)
            return data_validation_config
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def get_data_transformation_config(self)-> Data_Transformation_Config:
        try:
            pass
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def get_model_trainer_config(self)-> Model_Trainer_Config:
        try:
            pass
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def get_model_evaluation_config(self)->Model_Evaluation_Config:
        try:
            pass
        except Exception as e:
            raise Housing_Exception(e,sys) from e
    def get_model_pusher_config(self)-> Model_Pusher_Config:
        try:
            pass
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def get_training_pipeline_config(self)->Training_Pipeline_Config:
        try:
            training_pipeline_config=self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir= os.path.join(ROOT_DIR,
                                       training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                                       training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR])
            
            training_pipeline_config=Training_Pipeline_Config(artifact_dir=artifact_dir)
            logging.info(f"Training pipleine config: {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise Housing_Exception(e,sys) from e
