######################################################
#    프로그램명    : main.py
#    작성자        : GyuWon Hong
#    작성일자      : 2022.01.27
#    파라미터      : None
#    설명          : 카프카(producer, consumer)를 생성하여 받은 데이터를 전처리하고 카프카로 보내주는 전처리 모듈
######################################################

import json

from typing import List, Dict, Any, Optional

from kafka.kafka.kafka_session import create_producer, create_consumer
from preprocessing.patient_preprocessor import PatientPreprocessor
from utils.settings import KafkaConfig, ModelConfig
from utils.device_logger import logger

def dict_to_json(send_data: Dict[str, Any]):
    
    for key, value in send_data.items():
        if not isinstance(value, str):
            send_data[key] = str(value)
            
    send_data = json.dumps(send_data)

    return send_data

def main(args: Optional[List[str]] = None):

    # consumer 생성
    consumer = create_consumer(KafkaConfig.CONSUMER_TOPIC)

    # producer 생성
    producer = create_producer()

    running = True

    while running:

        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error("Consumer error: {}".format(msg.error()))
            continue

        msg_value = dict(msg_value.value())
        logger.info('Received message: {}'.format())

        # get patient name
        ptnt_no: str = msg_value['ptnt_no']

        # create or get existing patient instance
        patient_instance = PatientPreprocessor(ptnt_no)

        # input kafka data to instance's dataframe
        patient_instance.append_kafka_data(msg_value=msg_value)

        isEnough, isInit = patient_instance.isEnoughSize()

        if isEnough:
            # start instatnce's dataframe preprocessing
            patient_instance.start_preprocessing(isInit)
        else:
            continue
        
        send_data = patient_instance.get_msg_values(ModelConfig.SEND_SIZE)
        send_data = dict_to_json(send_data)

        producer.produce(KafkaConfig.PRODUCER_TOPIC, value=send_data)
        producer.flush()

    consumer.close()