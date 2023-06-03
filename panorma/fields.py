import pandas as pd


class StringDtype(pd.Series):
    pd_model = pd.StringDtype


class Float32Dtype(pd.Series):
    pd_model = pd.Float32Dtype


class Int16Dtype(pd.Series):
    pd_model = pd.Int16Dtype


class CategoricalDtype(pd.Series):
    pd_model = pd.CategoricalDtype


class Timestamp(pd.Series):
    pd_model = pd.Timestamp
