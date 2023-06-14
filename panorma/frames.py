import warnings
from typing import Tuple

import pandas as pd

from panorma.exceptions import NotMatchingFields, ParseError
from panorma.fields import Field


class DataFrame(pd.DataFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        warnings.filterwarnings('ignore')
        self.__class__.__name__ = "DataFrame"
        self._model_fields: dict[str, Field] = self.__class__.__dict__.get("__annotations__")
        self._df_dtypes_dict: dict = self.dtypes.to_dict()
        self._validate_fields_are_matching()
        self._validate_data_types()

    def _validate_fields_are_matching(self) -> None:
        """
        Check if the dataframe columns are matching the model fields. Raise exception if not
        """
        model_field_names = [key for key, value in self._model_fields.items()]
        columns = [col for col in self.columns]
        if sorted(model_field_names) != sorted(columns):
            raise NotMatchingFields(model_field_names, columns)

    def _validate_data_types(self) -> None:
        """
        Check if datatype of the fields are matching the types declared in the model. If not, try to cast.
        If not possible, raise a ParseError
        """
        for model_field_name, model_field_type in self._model_fields.items():
            try:
                df_field_name, df_field_type = self._get_matching_df_fields_name_and_type(model_field_name)
                if df_field_type in model_field_type.similar_types:
                    continue
                self[model_field_name] = model_field_type.convert(self[model_field_name])
            except Exception:
                raise ParseError(model_field_name, model_field_type)

    def _get_matching_df_fields_name_and_type(self, model_field_name: str) -> Tuple:
        df_field_type = self._df_dtypes_dict.get(model_field_name).type
        df_field_name = model_field_name
        return df_field_name, df_field_type
