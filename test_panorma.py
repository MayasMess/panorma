import unittest

import pandas as pd

from panorma.exceptions import NotMatchingFields, ParseError
from panorma.fields import String, Int, Float, DateTime, Categorical
from panorma.frames import DataFrame


class Users(DataFrame):
    name: String
    age: Int
    percentage: Float
    birth_date: DateTime


class Cars(DataFrame):
    car: String
    mpg: Float
    cylinders: Int
    displacement: Float
    horsepower: Float
    weight: Float
    acceleration: Float
    model: Int
    origin: Categorical


class TestPanorma(unittest.TestCase):
    def setUp(self) -> None:
        self.users_dict = {
            "name": ['john', 'kevin'],
            "age": [99, 15],
            "percentage": [0.8, 7.3],
            "birth_date": [pd.Timestamp('20180310'), pd.Timestamp('20230910')],
        }
        self.users_dict_with_missing_field = {
            "name": ['john', 'kevin'],
            "age": [99, 15],
            "birth_date": [pd.Timestamp('20180310'), pd.Timestamp('20230910')],
        }
        self.users_dict_with_wrong_data_types = {
            "name": ['john', 'kevin'],
            "age": [99, 15],
            "percentage": ["hello", "world"],
            "birth_date": [pd.Timestamp('20180310'), pd.Timestamp('20230910')],
        }
        self.users_dict_with_wrong_data_types_2 = {
            "name": ['john', 'kevin'],
            "age": [99, 15],
            "percentage": [0.8, 7.3],
            "birth_date": ["hello", "world"],
        }
        self.test_dataset = pd.read_csv("test_dataset.csv", sep=";")

    def test_instance_is_type_of_dataframe(self):
        users = Users(self.users_dict)
        self.assertIsInstance(users, pd.DataFrame)

    def test_model_fields_are_matching_with_columns__Should_Raise_NotMatchingFields(self):
        with self.assertRaises(NotMatchingFields):
            Users(self.users_dict_with_missing_field)

    def test_df_columns_are_convertible_to_model_field_types__Should_Raise_ParseError(self):
        with self.assertRaises(ParseError):
            Users(self.users_dict_with_wrong_data_types)
        with self.assertRaises(ParseError):
            Users(self.users_dict_with_wrong_data_types_2)

    def test_cars_dataset(self):
        cars = Cars(self.test_dataset.to_dict())
        self.assertAlmostEqual(float(cars.mpg.max()), 46.6, 5)

    def test_passing_dataframe_to_model(self):
        cars = Cars(self.test_dataset)
        self.assertIsInstance(cars, pd.DataFrame)
        self.assertAlmostEqual(float(cars.mpg.max()), 46.6, 5)
