import pandas as pd
import numpy as np
from typing import Protocol


class Field(Protocol):
    similar_types = []

    @classmethod
    def convert(cls, col: pd.Series) -> pd.Series:
        """Convert column to corresponding type"""


class String(pd.Series):
    similar_types = [str, pd.StringDtype, np.object_]

    @classmethod
    def convert(cls, col: pd.Series) -> pd.Series:
        return col.astype(str)


class Float(pd.Series):
    similar_types = [float, pd.Float32Dtype, pd.Float64Dtype, np.float32, np.float64]

    @classmethod
    def convert(cls, col: pd.Series) -> pd.Series:
        return col.astype(float)


class Int(pd.Series):
    similar_types = [int, pd.Int8Dtype, pd.Int16Dtype, pd.Int32Dtype, pd.Int64Dtype, np.int8, np.int16, np.int32,
                     np.int64]

    @classmethod
    def convert(cls, col: pd.Series) -> pd.Series:
        return col.astype(int)


class Categorical(pd.Series):
    similar_types = []

    @classmethod
    def convert(cls, col: pd.Series) -> pd.Series:
        return col.astype('category')


class DateTime(pd.Series):
    similar_types = [np.datetime64, pd.Timestamp, pd.DatetimeTZDtype]

    @classmethod
    def convert(cls, col: pd.Series) -> pd.Series:
        return pd.to_datetime(col)
