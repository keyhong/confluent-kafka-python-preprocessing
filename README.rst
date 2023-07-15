.. -*- mode: rst -*-

======================================
confluent-kafka-python-preprocessing
======================================

confluent-kafka-python 을 이용한 stateful 전처리 모듈

Installation
------------

.. code-block:: bash
    
  pip install -e . 

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
