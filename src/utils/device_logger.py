######################################################
#    프로그램명    : device_logger.py
#    작성자        : Gyu Won Hong
#    작성일자      : 2022.01.27
#    파라미터      : None
#    설명          : device 프로그램에 공통적으로 사용되는 logger 모듈
######################################################

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

file_handler = logging.FileHandler(__name__)
logger.addHandler(file_handler)