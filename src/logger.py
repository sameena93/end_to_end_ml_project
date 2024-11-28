import logging
import os
from datetime import datetime

LOGFILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"  #textfile naming convention will be created
logs_path = os.path.join(os.getcwd(),"logs", LOGFILE)  #LOG file path
os.makedirs(logs_path, exist_ok=True)   #if folder exists append the file



log_file_path = os.path.join(logs_path, LOGFILE)

logging.basicConfig(
    filename=log_file_path,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO,

)


