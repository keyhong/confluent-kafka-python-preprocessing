# confluent-kafka-python-preprocessing

[Confluent](https://www.confluent.io/ko-kr/?utm_medium=sem&utm_source=google&utm_campaign=ch.sem_br.brand_tp.prs_tgt.confluent-brand_mt.mbm_rgn.apac_lng.kor_dv.all_con.confluent-kafka-general&utm_term=confluent%20kafka&creative=&device=c&placement=&gad_source=1&gclid=EAIaIQobChMI7cLB7cmrhgMVBwh7Bx00aQ8XEAAYASAAEgKW8fD_BwE)사에서 만든 Kafka Python Client를 이용해 실시간으로 환자 데이터의 결측값을 보간하는 전처리 프로그램 <br> (**Note**: 기존 컬럼명에 대한 데이터 익명화 적용)



## Pacakge Build

```bash
$ pip install -e .
```

## Dependencies

requires:

| Lang | Version |
|------|---------|
| Python | 3.6+ |

**Note**: f-string을 사용하기 때문에 3.6 버전 이상의 파이썬에서 동작합니다.

| Package | Version | 
|---------|---------|
| numpy   | -       |
| pandas  | -       |
| scikit-learn | -  |
| confluent-kafka | 2.1.1 |

**Note**: preprocessing은 conflunet사에서 만든 `confluent-kafka` 라이브러리를 사용하고 있으며 버전은 2.2.1 입니다.
