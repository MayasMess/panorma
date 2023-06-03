import warnings

import pandas as pd

from panorma.exceptions import NotMatchingFields, ParseError


class DataFrame(pd.DataFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        warnings.filterwarnings('ignore')
        self.__class__.__name__ = "DataFrame"
        self._model_fields: dict = self.__class__.__dict__.get("__annotations__")
        self._df_dtypes_dict: dict = self.dtypes.to_dict()
        self._validate_fields_are_matching()
        self._validate_data_types()

    def _validate_fields_are_matching(self):
        model_field_names = [key for key, value in self._model_fields.items()]
        columns = [col for col in self.columns]
        if sorted(model_field_names) != sorted(columns):
            raise NotMatchingFields(model_field_names, columns)

    def _validate_data_types(self):
        for model_field_name, model_field_type in self._model_fields.items():
            try:
                df_field_type_name = self._df_dtypes_dict.get(model_field_name).name.lower()
                if model_field_type.__name__ == "Timestamp":
                    if "datetime" not in df_field_type_name:
                        self[model_field_name] = pd.to_datetime(self[model_field_name])
                    continue
                field_type_name = model_field_type.pd_model.name.lower()
                if field_type_name == df_field_type_name:
                    continue
                self[model_field_name] = self[model_field_name].astype(model_field_type.pd_model())
            except Exception:
                raise ParseError(model_field_name, model_field_type)
