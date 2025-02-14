import snowflake.connector as sc
from dotenv import load_dotenv
from pathlib import Path
import os 

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

class SnowflakeConnection:
    @staticmethod    
    def create_connection():
        con = sc.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            account=os.getenv("ACCOUNT"),
            database=os.getenv("DATABASE_NAME"),
            schema=os.getenv("SCHEMA"),
            role=os.getenv("ROLE_NAME")
        )
        return con
            
