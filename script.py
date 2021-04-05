"""
Load data from csv file.
Calculate a min, max, mean, sum of for each of the distinct values in specified column.
Save output to the csv file.
"""

import logging
import pandas as pd

from utilities.cleaner import Cleaner
from utilities.aggregator import Aggregator


def main(
    input_path: str,
    output_path: str,
    columns_info: dict,
    agg_col: str,
    values_col: str,
    aggregates: list,
    rename_cols: dict = None,
) -> None:
    """
    Load data from csv file, clean it and calculate min, max, avg values and sum
    for each of distinct values in given column.
    Save results to csv file afterwards.

    Parameters:
        * input_path (str): path to the csv file containing data to process
        * output_path (str): path to the csv file to save results in
        * columns_info (dict): dictionary containing information on input columns and
            their data types. (keys: column names, values: data types)
        * agg_col (str): name of the column to group data by
        * values_col (str): name of the column containing values to calculate aggregates
        * aggregates (list): list of aggregate calculations to apply
        * rename_cols (dict) (optional): if provided, columns will be renamed based on
            given info (keys: old column name, values: new column name)
    """
    logging.basicConfig(
        format="%(levelname)s   %(asctime)s   %(module)s:%(funcName)s\n%(message)s",
        level=logging.INFO,
    )

    logging.info(f"Reading data from: {input_path}.")
    dframe = pd.read_csv(input_path)

    logging.info(
        f"Creating instance of a cleaner with given columns info: {columns_info}."
    )
    cleaner = Cleaner(columns_info)
    logging.info(f"Created Cleaner instance: {cleaner}.")

    cleaner.validate_input(dframe)

    logging.info("Dropping missing values.")
    dframe = dframe.dropna()

    dframe = cleaner.list_from_string(dframe)
    dframe = cleaner.filter_uneven_rows(dframe)

    logging.info("Transforming elements of a list-like rows into separate rows.")
    dframe = dframe.apply(pd.Series.explode)

    dframe = cleaner.drop_empty_string(dframe)
    dframe = cleaner.convert_types(dframe)
    dframe = cleaner.filter_greater_than_zero(dframe)
    logging.info("Finished cleaning data!")

    aggregator = Aggregator(agg_col, values_col, aggregates)
    logging.info(f"Created Aggregator instance: {aggregator}.")

    aggregator.validate_input(dframe)
    dframe = aggregator.calculate_aggregates(dframe)
    logging.info("Finished cleaning data!")

    if rename_cols:
        logging.info(
            f"Renaming columns: {[*rename_cols.keys()]} to",
            f"{[*rename_cols.values()]} respectively.",
        )
        dframe.rename(columns=rename_cols, inplace=True)

    logging.info(f"Saving output data to: {output_path}.")
    dframe.to_csv(f"{output_path}", header=True, index=False)
    logging.info(f"Finished saving output data to: {output_path}.")


if __name__ == "__main__":
    main(
        input_path="input.csv",
        output_path="output.csv",
        columns_info={"hosts": "string", "values": "float"},
        agg_col="hosts",
        values_col="values",
        aggregates=["min", "max", "avg", "sum"],
        rename_cols={"hosts": "host"},
    )
