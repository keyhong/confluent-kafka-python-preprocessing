######################################################
#    프로그램명    : model_preprocessor_mixin.py
#    작성자        : GyuWon Hong
#    작성일자      : 2022.01.27
#    파라미터      : None
#    설명          : 전처리에 필요한 부수적인 기능을 지닌 Mixin 클래스
######################################################

from sklearn.preprocessing import MinMaxScaler
from utils.settings import DATA_DIR

__all__ = ["ModelPreprocessorMixin"]

class ModelPreprocessorMixin:

    def epa(self, vector: 'numpy.ndarray') -> 'numpy.ndarray':
        return (3 * (1 - vector ** 2) / 4) * (abs(vector) <=1)
 
    def storeMinMaxValue(self, df: 'pandas.core.frame.DataFrame') -> None:

        scaler = MinMaxScaler()
        scaler.fit(df)

        pd.DataFrame(
            data={'min': scaler.data_min_, 'max': scaler.data_max_},
            index=df.columns
        ).to_csv(os.path.join(DATA_DIR, self.patient, '_std.csv'), encoding='cp949')        
