import pandas as pd
import streamlit as st
from src.connection import SnowflakeConnection
from snowflake.connector.pandas_tools import write_pandas

snowflake_connection = SnowflakeConnection.create_connection()

def data_loading(file) -> pd.DataFrame:
    """Function to load data

    Args:
        file: Data

    Returns:
        DataFrame
    """
    file_df = pd.read_csv(file)
    snowparkDf = write_pandas(
        df=file_df,
        conn=snowflake_connection,
        table_name="ORGANIZATIONS",
        database="SQLPILOT",
        schema="PUBLIC",
        quote_identifiers=True,
        auto_create_table=True,
        overwrite=True
    )
    return snowparkDf


file = st.file_uploader("Upload your CSV file here", type={"csv"})
if file is not None:
    df = data_loading(file)
