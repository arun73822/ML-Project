from datetime import datetime
import os,sys

ROOT_DIR= os.getcwd()
CONFIG_DIR= "config"
CONFIG_FILE_NAME= "config.yaml"
CONFIG_FILE_PATH= os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%I-%M-%S_%p')}"

# Training_Pipeline_related_variables
TRAINING_PIPELINE_CONFIG_KEY= "training_pipeline_config"
TRAINING_PIPELINE_NAME_KEY= "pipeline_name"
TRAINING_PIPELINE_ARTIFACT_DIR= "artifact_dir"

# Data_Ingestion_related_variables
DATA_INGESTION_CONFIG_KEY= "data_ingestion_config"
DATA_INGESTION_DATASET_URL_KEY= "dataset_download_url"
DATA_INGESTION_RAW_DATA_DIR= "raw_data_dir"
DATA_INGESTION_TGZ_DATA_DIR= "tgz_data_dir"
DATA_INGESTION_INGESTED_DIR= "ingested_dir"
DATA_INGESTION_TRAIN_DATA_DIR= "ingested_train_dir"
DATA_INGESTION_TEST_DATA_DIR= "ingested_test_dir"
DATA_INGESTION_ARTIFACT_DIR= "data_ingestion"

# Data_Validation_related_variables
DATA_VALIDATION_CONFIG_KEY= "data_validation_config"
DATA_VALIDATION_SCHEMA_FILE_DIR= "schema_dir"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY= "schema_file_name"
DATA_VALIDATION_ARTIFACT_DIR= "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME_KEY= "report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY= "report_page_file_name"

# Data Transformation related variables
DATA_TRANSFORMATION_CONFIG_KEY= "data_transformation_config"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR= "transformed_train_dir"
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR= "transformed_test_dir"
DATA_TRANSFORMATION_PRE_PROCESSED_OBJECT_FILE_PATH_KEY= "preprocessed_object_file_name"

# Model trainer related variables
MODEL_TRAINER_CONFIG_KEY= "model_trainer_config"
MODEL_TRAINER_TRAINED_MODEL_DIR= "trained_model_dir"
MODEL_TRAINER_MODEL_FILE_NAME_KEY= "model_file_name"
MODEL_TRAINER_PREPROCESSED_OBJECT_FILE_NAME_KEY= "preprocessed_object_file_name"

# Model evaluation related variables
MODEL_EVALUATION_CONFIG_KEY= "model_evaluation_config"
MODEL_EVALUATION_MODEL_EVALUATION_FILE_NAME= "model_evaluation_file_name"

# Model_pusher related variables
MODEL_PUSHER_CONFIG_KEY= "model_pusher_config"
MODEL_PUSHER_MODEL_EXPORT_DIR= "model_export_dir"
