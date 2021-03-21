"""
Perform aggregate calculations on given pandas DataFrame.
Supports following aggregate calculations:
    * min - calculates min value from a group of elements
    * max - calculates max value from a group of elements
    * avg - calculates average (mean) value of a group of elements
    * sum - calculates sum of all elements
"""

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class Aggregator:
    """
    Perform aggregate calculations on given pandas DataFrame.
    Supports following aggregate calculations:
        * min - calculates min value from a group of elements
        * max - calculates max value from a group of elements
        * avg - calculates average (mean) value of a group of elements
        * sum - calculates sum of all elements
    Aggregate calculations can be extended through AGGREGATES_MAP by adding additional NumPy function.

    Instance variables:
        * agg_col (str): name of the dataframe column to group data by
        * values_col (str): name of the column containing values to calculate aggregates from
        * aggregates (list): list of strings of aggregate functions names
        * agg_funcs (list): list of aggregate functions objects based on passed "aggregates"
        * agg_names (list): list of aggregate functions names based on passed "aggregates"

    Methods:
        * validate_input: check if input dataframe contains columns passed as "agg_col" and "values_col"
        * calculate_aggregates: perform aggregate calculations,
            return grouped df with results in corresponding columns
    """

    AGGREGATES_MAP = {
        "min": np.min,
        "max": np.max,
        "avg": np.mean,
        "sum": np.sum,
    }

    def __init__(self, agg_col: str, values_col: str, aggregates: list):
        """
        Validate input aggregates and create an instance if no errors.

        Parameters:
            * agg_col (str): name of the dataframe column to group data by
            * values_col (str): name of the column containing values to calculate aggregates from
            * aggregates (list): list of strings of aggregate functions names

        Raises:
            * AssertionError if unsupported aggregate(s) in passed "aggregates" is/are found
        """
        self.aggregates = aggregates
        self._validate_aggregates(self.aggregates)
        self.agg_funcs = [
            v for k, v in self.AGGREGATES_MAP.items() if k in self.aggregates
        ]
        self.agg_names = [
            k for k, v in self.AGGREGATES_MAP.items() if k in self.aggregates
        ]
        self.agg_col = agg_col
        self.values_col = values_col

    def __repr__(self):
        return f'Aggregator calculating {self.agg_names} from "{self.values_col}" grouped by "{self.agg_col}" column.'

    def _validate_aggregates(self, aggregates: list) -> None:
        logger.info(
            f"Checking if each of the provided aggregates is supported. Supported aggregates are: {[*self.AGGREGATES_MAP.keys()]}."
        )
        supported_aggs = set(self.AGGREGATES_MAP.keys())
        input_aggs = set(aggregates)
        aggs_diff = input_aggs.difference(supported_aggs)
        assert (
            not aggs_diff
        ), f"Provided aggregate calculation(s): {aggs_diff} not supported. List of supported calculations: {[*self.AGGREGATES_MAP.keys()]}"

    def validate_input(self, dframe: pd.DataFrame) -> None:
        """
        Check if input dataframe contains columns for aggregate calculations.

        Parameters:
            * dframe (pd.DataFrame): dataframe to seek columns for aggregate calculations

        Raises:
            * AssertionError if some column for aggregate calculations is not found in dataframe
        """
        logger.info(
            f'Checking if input dataframe contains "{self.agg_col}" and "{self.values_col}" columns.'
        )
        for col in [self.agg_col, self.values_col]:
            assert col in [*dframe.columns], f"Input dataframe does not contain {col}."

    def calculate_aggregates(self, dframe: pd.DataFrame) -> pd.DataFrame:
        """
        Perform aggregate calculations.

        Parameters:
            * dframe (pd.DataFrame): dataframe with data to be grouped and used to perform calculations

        Returns:
            * dframe (pd.DataFrame): dataframe with grouped data and calculated aggregates
        """
        logger.info(
            f"Calculating: {self.agg_names} for: {self.values_col} grouped by: {self.agg_col}."
        )
        df_grouped = dframe.groupby(f"{self.agg_col}")
        dframe = df_grouped.agg({f"{self.values_col}": [*self.agg_funcs]}).reset_index()
        df_columns = [f"{self.agg_col}"]
        df_columns.extend(self.agg_names)
        dframe.columns = df_columns
        return dframe
