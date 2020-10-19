"""
Collection of helpers and fixtures for the test suite.
"""
import pandas as pd
import pytest
from utilities.cleaner import Cleaner
from utilities.aggregator import Aggregator


class Helpers:
    """
    Helper methods for the test suite.

    Methods:
        * df_equal: wraps pandas.testing.assert_frame equal with output more copliant to testing framework
    """

    @staticmethod
    def df_equal(left: pd.DataFrame, right: pd.DataFrame, **kwargs) -> bool:
        """
        Wrap pandas.testing.assert_frame_equal.
        pandas.testing.assert_frame_equal is wrapped because it returns None
        if no differences between dataframes are found.

        Parameters:
            * left (pd.DataFrame): DataFrame to compare.
            * right (pd.DataFrame): DataFrame to compare.

        Returns:
            * if dataframes are equal - True
            * if dataframes are not equal - raises AssertionError
        """
        pd.testing.assert_frame_equal(left, right, **kwargs)
        return True


@pytest.fixture
def helpers():
    """Return Helpers instance"""
    return Helpers()


@pytest.fixture
def cleaner():
    """Return pre-configured Cleaner instance"""
    return Cleaner(columns_info={"col_a": "string", "col_b": "float"})


@pytest.fixture
def aggregator():
    """Return pre-configured Aggregator instance"""
    return Aggregator(
        agg_col="col_a", values_col="col_b", aggregates=["min", "max", "avg", "sum"]
    )
