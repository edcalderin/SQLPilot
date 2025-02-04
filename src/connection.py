from sqlalchemy import create_engine
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class SnowflakeConnection:
    user: str
    password: str
    account: str
    
    def create_session(self):
        engine = create_engine(f"snowflake://{self.user}:{self.password}@{self.account}/")
        
        with engine.connect() as connection:
            try:
                results = connection.execute('SELECT CURRENT_VERSION()').fetchone()
                print(f"Connected to Snowflake. Version: {results[0]}")
                return connection
            except Exception as e:
                print(f"Error connecting to Snowflake: {e}")
                return None
            
