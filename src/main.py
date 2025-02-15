import streamlit as st
from src.connection import SnowflakeConnection

snowflake_connection = SnowflakeConnection()

file = st.file_uploader("Upload your CSV file here", type={"csv"})
if file is not None:
    df = snowflake_connection.data_loading(file)
    print("Data successfully saved!")
