import json
import pandas as pd
import streamlit as st
from src.connection import SnowflakeConnection
from dotenv import load_dotenv
import os

load_dotenv()

snowflake_connection = SnowflakeConnection(user=os.getenv(
    "USER"), password=os.getenv("PASSWORD"), account=os.getenv("ACCOUNT"))

session = snowflake_connection.create_session()

def data_loading(file) -> pd.DataFrame:
    """Function to load data

    Args:
        file: Data

    Returns:
        DataFrame
    """
    file_df = pd.read_csv(file)
    snowparkDf = session.write_pandas(
        file_df,
        table_name="ORGANIZATIONS",
        database="ORGANIZATIONS",
        schema="PUBLIC",
        quote_identifiers=True,
        auto_create_table=True,
        overwrite=True
    )
    return snowparkDf


file = st.file_uploader("Upload your CSV file here", type={"csv"})
if file is not None:
    df = data_loading(file)
