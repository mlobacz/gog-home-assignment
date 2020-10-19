"""utilities.aggregator test suite"""

import pandas as pd
import pytest
from utilities.aggregator import Aggregator


def test_validate_input_positive(aggregator):
    """
    Check if input dataframe contains columns for aggregate calculations
    with positive result.
    """
    input_df = pd.DataFrame(
        {
            "col_a": ["tosh2.moc", "tosh3.moc", "tosh1.moc", "tosh1.moc"],
            "col_b": [3063.33, 1301.62, 2137.21, 3214.43],
        }
    )
    aggregator.validate_input(input_df)

@pytest.mark.parametrize("col_1,col_2", [("wrong_col", "col_b"), ("col_a", "wrong_col")])
def test_validate_input_negative(aggregator, col_1, col_2):
    """
    Check if input dataframe contains columns for aggregate calculations
    with negative result.
    """   
    with pytest.raises(AssertionError):
        input_df = pd.DataFrame(
            {
                f"{col_1}": ["tosh2.moc", "tosh3.moc", "tosh1.moc", "tosh1.moc"],
                f"{col_2}": [3063.33, 1301.62, 2137.21, 3214.43],
            }
        )
        aggregator.validate_input(input_df)


@pytest.mark.parametrize(
    "input_aggs",
    [
        ["min", "max", "avg", "sum"],
        ["min", "max", "avg"],
        ["min", "max"],
        ["min"],
        ["sum", "avg", "max", "min"],
        ["sum", "avg", "max"],
        ["sum", "avg"],
        ["sum"],
    ],
)
def test_validate_aggregates_positive(input_aggs, aggregator):
    """Check if of provided aggregates is supported with positive result."""
    aggregator._validate_aggregates(input_aggs)


@pytest.mark.parametrize(
    "input_aggs",
    [
        ["agg_1", "agg_2"],
        ["agg_1", "agg_2", "agg_3", "agg_4"],
        ["min", "max", "avg", "sum", "agg_1"],
        ["min", "max", "agg_1", "agg_2"],
    ],
)
def test_validate_aggregates_negative(input_aggs, aggregator):
    """Check if of provided aggregates is supported with negative result."""
    with pytest.raises(AssertionError):
        aggregator._validate_aggregates(input_aggs)


@pytest.mark.parametrize(
    "aggregates,expected_df",
    [
        (
            ["min", "max", "avg", "sum"],
            pd.DataFrame(
                {
                    "col_a": ["tosh1.moc", "tosh2.moc", "tosh3.moc"],
                    "min": [1, 1, 3],
                    "max": [9, 2, 4],
                    "avg": [5, 1.5, 3.5],
                    "sum": [10, 3, 7],
                }
            ),
        ),
        (
            ["min", "max", "avg"],
            pd.DataFrame(
                {
                    "col_a": ["tosh1.moc", "tosh2.moc", "tosh3.moc"],
                    "min": [1, 1, 3],
                    "max": [9, 2, 4],
                    "avg": [5, 1.5, 3.5],
                }
            ),
        ),
        (
            ["min", "max"],
            pd.DataFrame(
                {
                    "col_a": ["tosh1.moc", "tosh2.moc", "tosh3.moc"],
                    "min": [1, 1, 3],
                    "max": [9, 2, 4],
                }
            ),
        ),
        (
            ["min"],
            pd.DataFrame(
                {
                    "col_a": ["tosh1.moc", "tosh2.moc", "tosh3.moc"],
                    "min": [1, 1, 3],
                }
            ),
        ),
    ],
)
def test_calculate_aggregates(helpers, aggregates, expected_df):
    """Perform calculations for aggregates."""
    aggregator = Aggregator(agg_col="col_a", values_col="col_b", aggregates=aggregates)
    input_df = pd.DataFrame(
        {
            "col_a": [
                "tosh2.moc",
                "tosh3.moc",
                "tosh1.moc",
                "tosh1.moc",
                "tosh2.moc",
                "tosh3.moc",
            ],
            "col_b": [1, 3, 9, 1, 2, 4],
        }
    )
    out_df = aggregator.calculate_aggregates(input_df)
    assert helpers.df_equal(expected_df, out_df)
