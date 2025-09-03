from logging.handlers import RotatingFileHandler
from logging import StreamHandler
import logging
from datetime import datetime

today = datetime.now().strftime("%d-%m-%Y")
filename = f"log/{today}.log"


def log_func():
    try:
        """
        This function is for console logging. It uses Streamhandler and level is debug.
        The Format of the logger is :- dd/mm/yyyy HH:MM:SS (AM/PM) mylogger (levelname) (message).
        It returns logger.    
        """
        logger = logging.getLogger("mylogger")
        logger.setLevel(logging.DEBUG)

        console = StreamHandler()
        console.setLevel(logging.DEBUG)

        handler = RotatingFileHandler(filename, mode= "a", encoding="UTF-8")
        handler.setLevel(logging.DEBUG)

        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

        console.setFormatter(format)
        handler.setFormatter(format)
        logger.addHandler(console)
        logger.addHandler(handler)
        return logger
    except Exception as e:
        print(e)

