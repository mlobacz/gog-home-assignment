"""
Clean data in given pandas DataFrame.
"""

import logging

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class Cleaner:
    """
    Clean data in given pandas DataFrame.

    Instance variables:
        * columns_info (dict): dictionary containing information on input columns
            and their data types. (keys: column names, values: data types)

    Methods:
        * validate_input: check if input dataframe contains columns provided in "columns_info"
        * list_from_string: transform dataframe elements from list-like looking strings into lists
        * filter_uneven_rows: filter out rows with uneven number of elements
        * filter_greater_than_zero: filter out rows with values in numeric columns not greater than 0
        * drop_empty_string: filter out rows with empty string values
        * convert_types: cast columns to provided types
    """

    NUMERIC_TYPES = ["float", "int"]

    def __init__(self, columns_info: dict):
        """
        Parameters:
            * columns_info (dict): dictionary containing information on input columns
                and their data types. (keys: column names, values: data types)
        """
        self.columns_info = columns_info

    def __repr__(self):
        return f"Cleaner for data with columns: {self.columns_info}"

    @staticmethod
    def _convert_to_list(value: str) -> list:
        logger.debug(f"Converting string: {value} to list.")
        return value.strip("[]").split(",")

    def validate_input(self, dframe: pd.DataFrame) -> None:
        """
        Check if input dataframe contains columns passed to cleaner with "columns_info".

        Parameters:
            * dframe (pd.DataFrame): dataframe to seek for columns in

        Raises:
            * AssertionError if dataframe columns do not match passed columns info
        """
        logger.info(
            f"Validating input data columns: {[*dframe.columns]} with provided columns: {[*self.columns_info.keys()]}."
        )
        assert [*dframe.columns] == [
            *self.columns_info.keys()
        ], "Dataframe columns do not match provided columns info."

    def list_from_string(self, dframe: pd.DataFrame) -> pd.DataFrame:
        """
        Convert each dataframe element from list-like looking string
        e.g.: "["value1","value2"]" into actual list.

        Parameters:
            * dframe (pd.DataFrame): dataframe where each element is list-like looking string

        Returns:
            * dframe (pd.DataFrame): dataframe with each element as a list
        """
        logger.info(
            "Converting each dataframe element from list-like looking string into list."
        )
        return dframe.applymap(self._convert_to_list)

    def filter_uneven_rows(self, dframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filter out rows with uneven number of elements.

        Parameters:
            * dframe (pd.DataFrame): dataframe where each element is a sequence or a collection

        Returns:
            * dframe (pd.DataFrame): dataframe with uneven rows filtered out
        """
        logger.info("Filtering out rows with uneven number of elements in columns.")
        dframe["length_diff"] = dframe.applymap(len).apply(np.diff, axis=1).apply(int)
        filt = dframe["length_diff"] == 0
        return dframe.loc[filt, [*self.columns_info.keys()]].reset_index(drop=True)

    def filter_greater_than_zero(self, dframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filter out rows with values in numeric columns not greater than 0.

        Parameters:
            * dframe (pd.DataFrame): dataframe with numeric (supported: "int" or "float") columns

        Returns:
            * dframe (pd.DataFrame): dataframe with non-positive values in numeric columns filtered out

        Raises:
            * AssertionError if no numeric columns ("int" or "float") are found in cleaners "columns_info"
        """
        numeric_columns = [
            k for k, v in self.columns_info.items() if v in self.NUMERIC_TYPES
        ]
        assert (
            numeric_columns
        ), f"No columns of numeric types in the provided columns_info. Numeric types are {self.NUMERIC_TYPES}."
        logger.info(
            f"Filtering out rows with values not greater than 0 in numeric columns: {numeric_columns}."
        )
        if len(numeric_columns) == 1:
            filt = dframe[numeric_columns[0]] > 0
        else:
            # FIXME: Raises "ValueError: Cannot index with multidimensional key"
            filt = dframe[numeric_columns] > 0
        return dframe.loc[filt].reset_index(drop=True)

    @staticmethod
    def drop_empty_string(dframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filter out rows with empty string values.

        Parameters:
            *dframe (pd.DataFrame): dataframe to filter out empty string values

        Returns:
            *dframe (pd.DataFrame): dataframe with empty string values filtered out
        """
        logger.info("Filtering out rows with empty string values.")
        dframe.replace("", np.nan, inplace=True)
        return dframe.dropna().reset_index(drop=True)

    def convert_types(
        self, dframe: pd.DataFrame, columns_info: dict = None
    ) -> pd.DataFrame:
        """
        Converts (casts) columns to given type.

        Parameters:
            *dframe (pd.DataFrame): dataframe to perform casting on
            *columns_info (dict) (optional): dictionary containing information on columns
                and their data types. (keys: column names, values: data types)

        Returns:
            *dframe (pd.DataFrame): dataframe after column casting
        """
        logger.info(
            f"Casting columns types based on given columns info: {self.columns_info}"
        )
        if columns_info:
            return dframe.astype(columns_info)
        else:
            return dframe.astype(self.columns_info)
