# GOG data processing home assignment

## Task description

Provided `input.csv` file contains data with two columns.
The first column contains a list of hosts and the second column contains a list of values in the same order as the first column.
Your goal is to calculate min value, max value, avg value and sum for each of those hosts.

## Solution description

Task was solved with help of `pandas` library and the self-developed [utilities](utilities) library based on `pandas`.

Complete processing of the input data resulting in the desired output is contained in the [script.py](script.py).

Section of the script presented below (starting at line 87) allows to customize performed processing.

```python
if __name__ == "__main__":
    main(
        input_path="input.csv",
        output_path="output.csv",
        columns_info={"hosts": "string", "values": "float"},
        agg_col="hosts",
        values_col="values",
        aggregates=["min", "max", "avg", "sum"],
        rename_cols={"hosts": "host"}
    )
```

Detailed information on each parameter can be found in the script's `main` function docstring.

Instead of writing only a script that would consume the input and produce desired output, I wanted to propose a design that would allow more flexibility in parametrization and possible future extensions. Thus, introduced [utilities](utilities) library that contains:

1. [Cleaner](utilities/cleaner.py) - collection of methods to clean given data.

2. [Aggregator](utilities/aggregator.py) - collection of methods to calculate aggregations on given data.

Details can be found in docstrings of each module.

## How to run tests and script

1. Clone this git repository

    ```bash
    git clone git@github.com:mlobacz/gog-home-assignment.git
    ```

2. Change into projects root directory.

    ```bash
    cd gog-gome-assignment
    ```

3. Create and activate new virtual environment

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

4. Install pip-tools

    ```bash
    pip install pip-tools
    ```

5. Install python requirements

    ```bash
    pip-sync requirements.txt dev-requirements.txt
    ```

6. Run tests followed by coverage report output

    ```bash
    pytest --cov=utilities tests/
    ```

7. Finally, run the script for yourself and see if you like the output ;) If you did not change script configuration it should be saved into `output.csv`. I also commited my results into [this file](output_ml.csv).

    ```bash
    python script.py
    ```
