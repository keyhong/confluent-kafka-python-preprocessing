#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

"""
config_parser를 이용하여 ".ini" 파일을 읽어들여 device의 상수 변수들을 정의한 모듈
"""

from __future__ import annotations

from preprocessing.utils._config_reader import ConfigReader 

__all__ = ["DirPath", "ModelConfig", "KafkaConfig"]

config_reader = ConfigReader()

# 폴더 경로
class DirPath:

    # 환경세팅 기본 폴더 절대경로
    ETL_HOME: str = ConfigReader.get_value('BASE_DIR', 'ETL_HOME')

    # 모델 스케일러 MIN, MAX값 저장 절대경로
    SCALER_DIR: str = ConfigReader.get_value('SCALER_DIR', 'SCALER_VALUE_DIR')

# 모델 옵션 설정
class ModelConfig:
    WINDOW_SIZE = int(config_reader.get_value("MODEL_OPTION", "WINDOW_SIZE"))
    BATCH_SIZE = int(config_reader.get_value("MODEL_OPTION", "BATCH_SIZE"))
    BAND_WIDTH = int(config_reader.get_value("MODEL_OPTION", "BAND_WIDTH"))
    SEND_SIZE = int(config_reader.get_value("MODEL_OPTION", "SEND_SIZE"))


# 카프카 브로커 연결 설정
class KafkaConfig:
    BOOTSTRAP_SERVER: str = f'{config_reader.get_value("KAFKA_OPTION", "HOST")}:{ConfigReader.get_value("KAFKA_OPTION", "PORT")}'
    GROUP_ID: str = config_reader.get_value("KAFKA_OPTION", "GROUP_ID") 
    PRODUCER_TOPIC: str = config_reader.get_value("KAFKA_OPTION", "PRODUCER_TOPIC")
    CONSUMER_TOPIC: str = config_reader.get_value("KAFKA_OPTION", "CONSUMER_TOPIC")
    
