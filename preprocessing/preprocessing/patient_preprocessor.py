#! -*- coding: utf-8 -*-

from __future__ import annotations

from datetime import datetime
import itertools
from typing import (
    Tuple,
    List,
    Dict,
    Union,
    Type,
)

import numpy as np
import pandas as pd

from preprocessing.model_preprocessor_mixin import ModelPreprocessorMixin
from preprocessing.utils.device_logger import logger
from preprocessing.utils.settings import ModelConfig

__all__ = ["PatientPreprocessor"]

class PatientPreprocessor(ModelPreprocessorMixin):

    # 싱글톤 패턴을 변형하여 새로운 환자가 있다면 새로 인스턴스를 만들고, 없다면 기존의 인스턴스를 반환 ( {gateway_number}: {데이터가 들어온 카운트 (연속성 확인)} )
    __instance: Dict[str, Type["PatientPreprocessor"]] = dict()

    # 명목형 변수 : 측정
    # 연속형 변수 : column1, column2, column3, column4, column5, column6, column7, column8

    df_vars: Dict[str, List[str]] = {
        "info": [ "tm", "hspt_id", "spce_id", "ptnt_no", "dvc_btry_rsdqy" ],
        "independent": [ "column1", "column2", "column3", "column4",  "column5", "column6", "column7" ]
    }

    def __new__(cls, ptnt_no: str):

        if not isinstance(ptnt_no, str):
            raise ValueError("ptnt_no must be str.")

        if ptnt_no in cls.__instance:
            return cls.__instance[ptnt_no]

        return super().__new__(cls)

    def __init__(
        self,
        ptnt_no: str,
        *args, **kwargs):

        if not hasattr(self, "ptnt_no"):
            self.ptnt_no = ptnt_no
            self.__df: pd.DataFrame = self._create_dataframe()
            self.__latest_append_datetime: Type[datetime.datetime] = None

            self.__instance[self.ptnt_no]: Dict[str, Type["PatientPreprocessor"]] = self
    
    def __del__(self):
        print(f"remove {self.ptnt_no} instance from class members.")
        # logger.info(f"remove {self.ptnt_no} instance from class members.")

    @classmethod
    def del_unspoorted_patient(cls):

        if not cls.__instance:
            return

        date_now = datetime.now()

        for key, value in cls.__instance.items():

            diff_days = (date_now - value.__latest_append_datetime).days

            if diff_days >= 3:
                cls.__instance.pop(key)

    @classmethod
    def _create_dataframe(cls) -> pd.DataFrame:

        dataFrame = pd.DataFrame(columns=list(itertools.chain(*cls.df_vars.values())))

        # type 변환 : np.float32 (nan 포함 허용, 값의 범위에 따라 부동소수점 포맷 조절)
        """
        - column1     | Min : 49    | Max : 197
        - column2     | Min : 23.7  | Max : 39.7
        - column3     | Min : 75    | Max : 100
        - column4     | Min : 0     | Max : 2184
        - column5     | Min : 28.0  | Max : 129.0
        - column6     | Min : 10.0  | Max : 129.0
        - column7     | Min : 111.0 | Max : 129.0
        - column8     | Min : 61.0  | Max : 79.0
        """
        dataFrame["column2"] = dataFrame["column2"].astype("UInt8")
        dataFrame["column4"] = dataFrame["column4"].astype("UInt16")

        cols: List[str] = [ "column1", "column3", "column5", "column6", "column7" ]
        dataFrame[cols] = dataFrame[cls.df_vars["independent"]].astype(np.float32)

        return dataFrame

    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self, df):
        self.__df = df

    def append_kafka_data(self, msg_value: Dict[str, Union[str, int]]):

        # 데이터를 넣는다
        row_data = pd.DataFrame(np.array([list(msg_value.values())]), columns=msg_value.keys())

        cols: List[str] = self.df_vars["independent"] + self.df_vars["addition"]
        row_data[cols] = row_data[cols].astype(np.float32)
        self.__df = pd.concat([self.__df, row_data], axis=0, ignore_index=True)

        # 데이터의 추가 일자를 최신으로 동기화 시킨다
        self.__latest_append_datetime = datetime.now()

        # 데이터프레임이 212개 보다 많은 경우
        if ModelConfig.BATCH_SIZE < len(self.__df):
            self.__df = self.__df.drop(index=0, axis=0).reset_index(drop=True)
        # 데이터프레임이 ModelConfig.WINDOW_SIZE(12개)인 경우
        elif len(self.__df) == ModelConfig.WINDOW_SIZE:
            self.check_initialize_window()
        else:
            return

    def isEnoughSize(self) -> Tuple[bool, bool]:

        if ModelConfig.WINDOW_SIZE == len(self.__df):
            return (True, True)

        if  ModelConfig.WINDOW_SIZE < len(self.__df):
            return (True, False)

        return (False, False)

    def start_preprocessing(self, isInit=False):

        # 측정 시간 전처리
        self._time_preprocessing(isInit)

        # column2 전처리
        self._temperature_preprocessing(isInit)

        # column4 전처리
        self._steps_preprocessing(isInit)

        # 결측값 보간 전처리
        self._impute_missing_value()

    def check_initialize_window(self):

        null_count : pd.Series = self.__df.isnull().sum()

        for count in null_count.array:
            if count == ModelConfig.WINDOW_SIZE:
                self.__df = self.__df.drop(index=0, axis=0).reset_index(drop=True)
                break

    def _time_preprocessing(self, isInit: bool=False):

        if isInit:
            self.__df["msrt_dtm"] = pd.to_datetime(self.__df["msrt_dtm"])
            self.__df["msrt_dtm"] = self.__df["msrt_dtm"].dt.hour * 60 + self.__df["msrt_dtm"].dt.minute
        else:
            last_msrt_dtm: "pandas.Timestamp" = pd.to_datetime(self.__df["msrt_dtm"].iat[-1])
            self.__df["msrt_dtm"].iat[-1] = last_msrt_dtm.hour * 60 + last_msrt_dtm.minute

    def _temperature_preprocessing(self, isInit: bool=False):

        if isInit:
            self.__df["column2_pre"] = np.where(self.__df["column2"] <= 30, np.nan, self.__df["column2"])
        else:
            self.__df["column2_pre"].iat[-1] = np.nan if self.__df["column2"].iat[-1] <= 30 else self.__df["column2"].iat[-1]

    def _steps_preprocessing(self, isInit: bool=False):

        if isInit:
            # 마지막 column4 저장
            self.__last_steps: int = self.__df["column4"].iat[-1]
            self.__df["column4_pre"] = self.__df["column4"].diff()

            # diff() 후 처음 값에 0 대입
            self.__df["column4_pre"].iat[0] = 0

            # column4 차분 값이 0 보다 작은 값들은 0으로 변경
            self.__df["column4_pre"] = np.where(self.__df["column4_pre"] < 0, 0, self.__df["column4_pre"])
        else:
            preprocessed_steps: int = self.__df["column4"].iat[-1] - self.__last_steps
            self.__last_steps = self.__df["column4"].iat[-1]

            self.__df["column4_pre"].iat[-1] = 0 if preprocessed_steps < 0 else preprocessed_steps

    def _impute_missing_value(self):

        # "independent": [ "column1", "column2", "column3", "column4",  "column5", "column6", "column7" ]
        imputation_vars: List[str] = [ col + "_pre" if col in ("column4", "column2") else col for col in self.df_vars["independent"] ]

        for col in imputation_vars:
            temp_series: pd.Series = self.__df[col]

            na_indexes: pd.Series = temp_series.iloc[-12:]
            na_indexes: pd.core.indexes.numeric.Int64Index = na_indexes[na_indexes.isna()].index

            no_na_indexes: pd.core.indexes.numeric.Int64Index = temp_series[~temp_series.index.isin(na_indexes)].index

            for na_index in na_indexes:

                vector_value: np.ndarray = (no_na_indexes - na_index).values / 200
                weight_epa: np.ndarray = self.epa(vector=vector_value) / ModelConfig.BAND_WIDTH
                fill_value: np.float64 = np.sum(weight_epa * temp_series.values[no_na_indexes]) / np.sum(weight_epa)
                self.__df.loc[na_index, col] = round(fill_value, 3)


    def get_msg_values(self, SEND_SIZE: int) -> Dict[str, str]:
        
        REV_SEND_SIZE = (-1) * SEND_SIZE
        imputation_vars: List[str] = [ col + "_pre" if col in ("column4", "column2") else col for col in self.df_vars["independent"] ]

        input_values: pd.DataFrame = self.__df.iloc[REV_SEND_SIZE:].loc[:, imputation_vars]
        input_values = input_values.applymap(lambda x: round(x, 3))

        # 1차원 문자열 array로 변환
        input_values: np.ndarray = input_values.values.flatten().astype(str)

        # "," 을 구분자로 값을 이어붙인 문자열 생성
        input_values: str = ",".join(input_values)

        # dict(patient_instance.df.iloc[-1])
        original_cols = list(itertools.chain(*self.df_vars.values()))
        msg_values: Dict[str, str] = dict(self.__df.iloc[-1][original_cols])
        msg_values["input_values"] = input_values
        
        return msg_values