from collections import namedtuple

Data_Ingestion_Artifact=namedtuple("Data_Ingestion_Artifact",['train_file_path','test_file_path',
                                                              'is_ingested','message'])
