from collections import namedtuple

Data_Ingestion_Artifact=namedtuple("Data_Ingestion_Artifact",['train_file_path','test_file_path',
                                                              'is_ingested','message'])

Data_Validation_Artifact=namedtuple("Data_Validation_Artifact",['schema_file_path','report_file_path',
                                                                'report_page_file_path','is_validated',
                                                                'message'])
