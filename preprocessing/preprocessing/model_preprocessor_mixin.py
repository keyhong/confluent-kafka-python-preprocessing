#! -*- coding: utf-8 -*-

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from preprocessing.utils.settings import DirPath

__all__ = ["ModelPreprocessorMixin"]

class ModelPreprocessorMixin:

    def epa(self, vector: np.ndarray) -> np.ndarray:
        return (3 * (1 - vector ** 2) / 4) * (abs(vector) <=1)
 
    def storeMinMaxValue(self, df: pd.DataFrame) -> None:

        scaler = MinMaxScaler()
        scaler.fit(df)

        pd.DataFrame(
            data={"min": scaler.data_min_, "max": scaler.data_max_},
            index=df.columns
        ).to_csv(os.path.join(DirPath.DATA_DIR, self.patient, "_std.csv"), encoding="cp949")        
