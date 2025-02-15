# SQL Pilot
Text2Sql application using llama-index and Snowflake with Streamlit.

## Requirements
**Python 3.11** and **Poetry**

## Setting up env

Run:
* If you do not have Python 3.11, use `conda` to create a new environment or install it from the official website, and then run `poetry env use` command so that poetry uses it as context.

* ```poetry config virtualenvs.in-project true```

* ```poetry install```

## Running the app

* Rename `.env.example` to `.env` and complete the variables according your Snowflake credentials:

```
USER=
PASSWORD=
SCHEMA=
DATABASE_NAME=
ACCOUNT=
ROLE_NAME=
WAREHOUSE_NAME=
TABLE_NAME=
OPENAI_API_KEY=<openai-api-key>
```

* Start the app:  
```python -m streamlit run src/main.py```

## Lint
Run:
* ```ruff format .```
* ```ruff check . --fix```