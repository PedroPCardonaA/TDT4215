from IPython.display import display
import polars as pl
import numpy as np

def perform_eda(df: pl.DataFrame, name: str = "DataFrame") -> None:
    """
    Perform exploratory data analysis on the provided Polars DataFrame.

    This function prints and displays the DataFrame's schema, summary statistics,
    head (first few rows), and null counts in a Jupyter-friendly format.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to analyze.
    name : str, optional
        A descriptive name for the DataFrame (default is "DataFrame").
    """
    # Print the DataFrame name.
    print(f"=== {name} ===\n")

    # 1. Display the schema by creating a summary table of column names and their dtypes.
    print("-- Schema --")
    schema_data = {
        "Column": list(df.schema.keys()),
        "Dtype": [str(dtype) for dtype in df.schema.values()]
    }
    schema_df = pl.DataFrame(schema_data)
    display(schema_df.to_pandas())

    # 2. Display summary statistics as a table.
    print("\n-- Describe --")
    describe_df = df.describe()
    display(describe_df.to_pandas())

    # 3. Display the first few rows of the DataFrame.
    print("\n-- Head --")
    head_df = df.head()
    display(head_df.to_pandas())

    # 4. Display the count of null values in each column.
    print("\n-- Null Counts --")
    null_counts_df = df.null_count()
    display(null_counts_df.to_pandas())


def data_sparsity(behavior_df: pl.DataFrame) -> float:
    """
    Calculate the sparsity of a user-item interaction DataFrame.

    The function first removes duplicate interactions (based on the same user_id and article_id)
    and then computes sparsity as one minus the ratio of unique interactions to the total possible
    interactions (i.e., number of users multiplied by number of items).

    Parameters
    ----------
    behavior_df : pl.DataFrame
        The user-item interaction DataFrame.

    Returns
    -------
    float
        The sparsity of the DataFrame.
    """
    # Remove duplicate interactions based on "user_id" and "article_id".
    unique_behavior_df = behavior_df.unique(subset=["user_id", "article_id"])
    # Compute the number of unique interactions.
    num_interactions = unique_behavior_df.shape[0]
    # Compute the number of unique users.
    num_users = unique_behavior_df["user_id"].n_unique()
    # Compute the number of unique items.
    num_items = unique_behavior_df["article_id"].n_unique()
    # Calculate sparsity as one minus the ratio of interactions to the total possible interactions.
    sparsity = 1 - (num_interactions / (num_users * num_items))
    return sparsity
