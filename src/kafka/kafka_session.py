import socket
from collections import abc
from typing import Dict, Union, Iterable, Optional, Any


from confluent_kafka import SerializingProducer, DeserializingConsumer
from confluent_kafka.serialization import StringSerializer, StringDeserializer

from utils.settings import KafkaConfig

__all__ = ["create_consumer", "create_producer"]

def __isStr(str_obj) -> str:

    if not isinstance(str_obj, str):
        raise ValueError(f'topic {string} is not string.')

    return str_obj


def create_producer(config=Optional[Dict[str, Any]]) -> 'confluent_kafka.SerializingProducer':

    # serializer define
    serializer = StringSerializer('utf_8')
    
    # kafka producer initialize
    producer_config = {
        'bootstrap.servers': KafkaConfig.BOOTSTRAP_SERVER,
        'key.serializer': serializer,
        'value.serializer': serializer,
        'client.id': socket.gethostname()
    }
    producer = SerializingProducer(producer_config)

    return producer    
        
def create_consumer(consumer_topic: Union[str, Iterable[str]], config=Optional[Dict[str, Any]]) -> 'confluent_kafka.DeserializingConsumer':

    if isinstance(consumer_topic, str):
        topics = [ consumer_topic ]
    elif isinstance(consumer_topic, abc.Iterable):
        topics = [ __isStr(topic) for topic in consumer_topic ]
    else:
        raise ValueError(f'topics must be string or Iterable Object')
    
    # deserializer define
    deserializer = StringDeserializer('utf_8')
    
    # kafka consumer initialize
    consumer_config = {
        'bootstrap.servers': KafkaConfig.BOOTSTRAP_SERVER,
        'group.id': KafkaConfig.GROUP_ID,
        'key.deserializer': deserializer,
        'value.deserializer': deserializer,
        'enable.auto.commit': True,
        'client.id': socket.gethostname(),
        'auto.offset.reset': 'earliest'
        # auto.commit.interval.ms : commit interval 시간
    }
    
    consumer = DeserializingConsumer(consumer_config)
    consumer.subscribe(topics)

    return consumer