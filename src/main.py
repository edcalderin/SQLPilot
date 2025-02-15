import streamlit as st
from src.connection import SnowflakeConnection
import pandas as pd
import re

snowflake_connection = SnowflakeConnection()

file = st.file_uploader("Upload your CSV file here", type={"csv"})


def add_snowflake_quotes(sql):
    # Split into main part and ORDER BY part
    parts = re.split(r'\bORDER BY\b', sql, flags=re.IGNORECASE)
    main_sql = parts[0]
    
    # Handle the main query part
    # Add quotes around column names before AS
    main_sql = re.sub(r'(?<!")\b([A-Za-z]\w*)(?!")\b(?=\s+AS|\s*[,)]|\s+(?:FROM|GROUP BY)|\s*$)', r'"\1"', main_sql)
    
    # Remove quotes from aliases after AS
    main_sql = re.sub(r'AS\s+"([^"]+)"', r'AS \1', main_sql)
    
    # Add quotes around table names
    main_sql = re.sub(r'(FROM|JOIN)\s+(?<!")([A-Za-z]\w*)(?!")', r'\1 "\2"', main_sql)
    
    # Reconstruct with ORDER BY if it exists
    if len(parts) > 1:
        # Don't add quotes to ORDER BY columns
        sql = f"{main_sql} ORDER BY {parts[1]}"
    else:
        sql = main_sql
        
    return sql

if file is not None:
    print("Loading data")
    df = snowflake_connection.data_loading(file)
    if df is not None:
        print("Creating Query Engine")
        engine, query_engine = snowflake_connection.data_querying()
        question = st.text_area("Enter your question here")
        if question:
            print("Querying...")
            response = query_engine.query(question)
            sql_query = response.metadata["sql_query"]
            sql_query = add_snowflake_quotes(sql_query)
            with engine.connect() as con:
                print(sql_query, response)
                df = pd.read_sql(sql_query, con)

            st.write(df)
