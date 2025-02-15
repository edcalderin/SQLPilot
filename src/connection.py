import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.settings import Settings
from llama_index.llms.openai import OpenAI
from snowflake.snowpark.session import Session
from sqlalchemy import create_engine

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)


class SnowflakeConnection:
    """Class for Snowflke connection."""

    @staticmethod
    def _credentials() -> dict:
        return dict(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            account=os.getenv("ACCOUNT"),
            database=os.getenv("DATABASE_NAME"),
            schema=os.getenv("SCHEMA"),
            role=os.getenv("ROLE_NAME"),
        )

    def _create_session(self) -> Session:
        return Session.builder.configs(self._credentials()).create()

    def data_loading(self, file):
        """Load data."""
        df: pd.DataFrame = pd.read_csv(file)
        session: Session = self._create_session()
        snowpark_df = session.write_pandas(
            df,
            table_name=os.getenv("TABLE_NAME"),
            database=os.getenv("DATABASE_NAME"),
            schema=os.getenv("SCHEMA"),
            quote_identifiers=True,
            auto_create_table=True,
            overwrite=True,
        )
        return snowpark_df

    def data_querying(self):
        """Query data with llama-index."""
        credentials: dict = self._credentials()
        snowflake_uri: str = f"snowflake://{credentials.get('user')}:{credentials.get('password')}@{credentials.get('account')}/{credentials.get('database')}/{credentials.get('schema')}?warehouse={os.getenv('WAREHOUSE_NAME')}&role={credentials.get('role')}"

        Settings.llm = OpenAI(model="gpt-4o", temperature=0)
        Settings.chunk_size = 1024

        engine = create_engine(snowflake_uri)
        sql_database = SQLDatabase(engine)
        query_engine = NLSQLTableQueryEngine(
            sql_database=sql_database, tables=[os.getenv("TABLE_NAME")]
        )
        return engine, query_engine
