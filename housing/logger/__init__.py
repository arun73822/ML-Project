import logging
import os
from datetime import datetime

LOG_DIR= 'housing_logs'
CURRENT_TIME_STAMP= f"{datetime.now().strftime('%d-%m-%Y_%I:%M:%S_%p')}"
LOG_FILE_NAME= f"log_{CURRENT_TIME_STAMP}.log"

os.makedirs(LOG_DIR,exist_ok=True)

LOG_FILE_PATH= os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(filename=LOG_FILE_PATH,filemode='w',level=logging.INFO,
                    format='[%(asctime)s] %(name)s - %(levelname)s - %(messages)s')
