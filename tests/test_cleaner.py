"""utilities.cleaner test suite"""
import pytest
import pandas as pd
from utilities.cleaner import Cleaner


def test_validate_input_positive(cleaner):
    """
    Validate input dataframe against correct columns_info
    with positive result.
    """
    input_df = pd.DataFrame(
        {
            "col_a": [
                "['tosh1.moc']",
                "['tosh2.moc','tosh4.moc']",
                "['tosh1.moc','tosh4.moc','tosh1.moc','tosh4.moc']",
            ],
            "col_b": [
                "[3063.33]",
                "[1301.62,9203.05]",
                "[7026.18,6647.35,9618.39,8697.18]",
            ],
        }
    )
    cleaner.validate_input(input_df)


def test_validate_input_negative():
    """
    Validate input dataframe against incorrect columns_info
    with negative result.
    """
    input_df = pd.DataFrame(
        {
            "col_a": [
                "['tosh1.moc']",
                "['tosh2.moc','tosh4.moc']",
                "['tosh1.moc','tosh4.moc','tosh1.moc','tosh4.moc']",
            ],
            "col_b": [
                "[3063.33]",
                "[1301.62,9203.05]",
                "[7026.18,6647.35,9618.39,8697.18]",
            ],
        }
    )

    wrong_info = {"not_col_a": "string", "col_b": "float"}
    cleaner = Cleaner(columns_info=wrong_info)
    with pytest.raises(AssertionError):
        cleaner.validate_input(input_df)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("['tosh2.moc','tosh4.moc']", ["'tosh2.moc'", "'tosh4.moc'"]),
        ("[1301.62,9203.05]", ["1301.62", "9203.05"]),
    ],
)
def test_convert_to_list(cleaner, test_input, expected):
    """Convert from list-like looking string into actual list."""
    out_list = cleaner._convert_to_list(test_input)  # pylint: disable = W0212
    assert isinstance(out_list, list)
    assert out_list == expected


def test_list_from_string(helpers, cleaner):
    """
    Convert each dataframe element from list-like looking string
    into actual list.
    """
    input_df = pd.DataFrame(
        {
            "col_a": [
                "['tosh1.moc']",
                "['tosh2.moc','tosh4.moc']",
                "['tosh1.moc','tosh4.moc','tosh1.moc','tosh4.moc']",
            ],
            "col_b": [
                "[3063.33]",
                "[1301.62,9203.05]",
                "[7026.18,6647.35,9618.39,8697.18]",
            ],
        }
    )

    expected = pd.DataFrame(
        {
            "col_a": [
                ["'tosh1.moc'"],
                ["'tosh2.moc'", "'tosh4.moc'"],
                ["'tosh1.moc'", "'tosh4.moc'", "'tosh1.moc'", "'tosh4.moc'"],
            ],
            "col_b": [
                ["3063.33"],
                ["1301.62", "9203.05"],
                ["7026.18", "6647.35", "9618.39", "8697.18"],
            ],
        }
    )
    out_df = cleaner.list_from_string(input_df)
    assert helpers.df_equal(out_df, expected)


def test_filter_uneven_rows(helpers, cleaner):
    """Filter out rows with uneven number of elements"""
    input_df = pd.DataFrame(
        {
            "col_a": [
                ["'tosh1.moc'"],
                ["'tosh2.moc'", "'tosh4.moc'"],
                ["'tosh1.moc'", "'tosh4.moc'", "'tosh1.moc'", "'tosh4.moc'"],
                ["'tosh1.moc'", "'tosh4.moc'", "'tosh1.moc'", "'tosh4.moc'"],
            ],
            "col_b": [
                ["3063.33"],
                ["1301.62"],
                ["7026.18", "6647.35", "9618.39", "8697.18"],
                ["7026.18", "6647.35", "9618.39"],
            ],
        }
    )
    expected_df = pd.DataFrame(
        {
            "col_a": [
                ["'tosh1.moc'"],
                ["'tosh1.moc'", "'tosh4.moc'", "'tosh1.moc'", "'tosh4.moc'"],
            ],
            "col_b": [
                ["3063.33"],
                ["7026.18", "6647.35", "9618.39", "8697.18"],
            ],
        }
    )
    out_df = cleaner.filter_uneven_rows(input_df)
    assert helpers.df_equal(out_df, expected_df)


def test_filter_greater_than_zero(helpers, cleaner):
    """Filter out rows with non-positive values in numeric column."""
    input_df = pd.DataFrame(
        {
            "col_a": ["0", "tosh1.moc", "tosh2.moc", "tosh1.moc"],
            "col_b": [3063.33, -1, 1301.62, 0],
        }
    )

    expected_df = pd.DataFrame(
        {
            "col_a": ["0", "tosh2.moc"],
            "col_b": [3063.33, 1301.62],
        }
    )

    out_df = cleaner.filter_greater_than_zero(input_df)
    assert helpers.df_equal(out_df, expected_df)


@pytest.mark.xfail()
def test_filter_greater_than_zero_2_num_cols(helpers):
    """
    Filter out rows with non-positive values in numeric columns,
    when there are is more than one numeric columns.
    Now failing with: ValueError: Cannot index with multidimensional key.
    """
    cleaner = Cleaner(columns_info={"col_a": "float", "col_b": "float"})
    input_df = pd.DataFrame(
        {
            "col_a": [3, 2, 0, 1],
            "col_b": [3063.33, -1, 1301.62, 0],
        }
    )

    expected_df = pd.DataFrame(
        {
            "col_a": [3],
            "col_b": [3063.33],
        }
    )

    out_df = cleaner.filter_greater_than_zero(input_df)
    assert helpers.df_equal(out_df, expected_df)


def test_filter_greater_than_zero_no_numeric_cols():
    """Raise AssertionError when there are no numeric columns in cleaner column_info."""
    cleaner = Cleaner(columns_info={"col_a": "string", "col_b": "string"})
    input_df = pd.DataFrame(
        {
            "col_a": ["0", "tosh1.moc", "tosh2.moc", "tosh1.moc"],
            "col_b": [3063.33, -1, 1301.62, 0],
        }
    )

    with pytest.raises(AssertionError):
        cleaner.filter_greater_than_zero(input_df)


def test_drop_empty_string(helpers, cleaner):
    """Filter out rows with empty string values."""
    input_df = pd.DataFrame(
        {
            "col_a": ["0", "", "tosh1.moc", "tosh1.moc"],
            "col_b": [3063.33, 1301.62, -1, 0],
        }
    )

    expected_df = pd.DataFrame(
        {
            "col_a": ["0", "tosh1.moc", "tosh1.moc"],
            "col_b": [3063.33, -1, 0],
        }
    )

    out_df = cleaner.drop_empty_string(input_df)
    assert helpers.df_equal(out_df, expected_df)


def test_convert_types(helpers, cleaner):
    """Convert column types to types passed in cleaner setup."""
    input_df = pd.DataFrame(
        {
            "col_a": ["0", "", "tosh1.moc", "tosh1.moc"],
            "col_b": ["3063.33", "1301.62", "-1", "0"],
        }
    )
    expected_df = pd.DataFrame(
        {
            "col_a": ["0", "", "tosh1.moc", "tosh1.moc"],
            "col_b": [3063.33, 1301.62, -1, 0],
        }
    ).astype({"col_a": "string", "col_b": "float"})

    out_df = cleaner.convert_types(input_df)

    assert helpers.df_equal(out_df, expected_df)


def test_convert_types_given_info(helpers, cleaner):
    """Convert column types when info passed directly to the method."""
    input_df = pd.DataFrame(
        {
            "col_a": ["0", "", "tosh1.moc", "tosh1.moc"],
            "col_b": [3063.33, 1301.62, -1, 0],
        }
    )
    expected_df = pd.DataFrame(
        {
            "col_a": ["0", "", "tosh1.moc", "tosh1.moc"],
            "col_b": ["3063.33", "1301.62", "-1.0", "0.0"],
        }
    ).astype({"col_a": "string", "col_b": "string"})

    test_info = {"col_a": "string", "col_b": "string"}
    out_df = cleaner.convert_types(input_df, columns_info=test_info)
    assert helpers.df_equal(out_df, expected_df)
