.. -*- mode: rst -*-

======================================
confluent-kafka-python-preprocessing
======================================

confluent-kafka-python 을 이용한 stateful 전처리 모듈

Installation
------------

.. code-block:: bash
    
  cd /home/icitydatahub/soss && pip install -e . 

Execution
-----------
| 프로그램을 실행시키기 위한 일별, 월별 프로그램을 실행시킬수 있는 airflow 스케줄링 파일 ($AIRFLOW_HOME/dags)이 만들어져 있습니다.
| 따라서 스케줄링을 실행하고 airflow-webserver 에서 실행 확인 필요
| airflow-webserver : http://172.19.100.217:8080/home

Dependencies
------------

soss requires python :

- Python (>= 3.6)

**preprocessing은 f-string을 사용하기 때문에 Python 3.6 버전 이상의 파이썬에서 동작합니다.**

soss requires packages:

- numpy
- pandas
- scikit-learn
- confluent-kafka 2.1.1

**preprocessing은 conflunet사에서 만든 confluent-kafka 라이브러리를 사용하고 있으며 버전은 2.2.1 입니다.**