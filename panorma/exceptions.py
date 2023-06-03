class NotMatchingFields(Exception):
    msg = "Fields of the dataframe are not matching the fields of the model"

    def __init__(self, model_field_names: list, columns: list):
        msg = self.msg + f"\n model => {model_field_names} \n columns => {columns}"
        super(NotMatchingFields, self).__init__(msg)


class ParseError(Exception):
    def __init__(self, field_name, field_type):
        msg = f"Impossible to parse {field_name} to {field_type}"
        super(ParseError, self).__init__(msg)
