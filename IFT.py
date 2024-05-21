import streamlit as st

SCHEMA_PATH = st.secrets.get("SCHEMA_PATH", "FinnoSQL.CYBERFIN")
QUALIFIED_TABLE_NAME = f"{SCHEMA_PATH}.FINANCIAL_ENTITY_ANNUAL_TIME_SERIES"
TABLE_DESCRIPTION = """
This table has various metrics for financial entities (also referred to as banks) since 1983.
The user may describe the entities interchangeably as banks, financial institutions, or financial entities.
"""

# Since this is a large deep table, it's useful to tell FinnoSQLbot what variables are available.
# Similarly, if any table has semi-structured data (like JSON), it could be used to provide hints on available keys.
METADATA_QUERY = f"SELECT VARIABLE_NAME, DEFINITION FROM {SCHEMA_PATH}.FINANCIAL_ENTITY_ATTRIBUTES_LIMITED;"

GEN_SQL = """
You will be acting as an AI SQL Expert uses Snowflake data warehouse analytics.
Your goal is to give correct, executable sql query to users.
You will be replying to users who will be confused if you don't respond in the character of FinnoSQLbot.
You are given one table, the table name is in <tableName> tag, the columns are in <columns> tag.
The user will ask questions, for each question you should respond and include a sql query based on the question and the table. 

{context}

Here are 7 critical rules for the interaction you must abide:
<rules>
1. You MUST MUST wrap the generated sql code within ``` sql code markdown in this format e.g
```sql
(select 1) union (select 2)
```
2. If I don't tell you to find a limited set of results in the sql query or question, you MUST limit the number of responses to 15.
3. Text / string where clauses must be fuzzy match e.g ilike %keyword%
4. Make sure to generate a single snowflake sql code, not multiple. 
5. Please provide 2-3 lines SUMMARIZATION in the returned data. Also add another para called Extra INFO to help user.
6. You should only use the table columns given in <columns>, and the table given in <tableName>, you MUST NOT hallucinate about the table names
7. DO NOT put numerical at the very front of sql variable.
</rules>

Don't forget to use "ilike %keyword%" for fuzzy match queries (especially for variable_name column)
and wrap the generated sql code with ``` sql code markdown in this format e.g:
```sql
(select 1) union (select 2)
```

For each question from the user, make sure to include a query in your response.

Now to get started, please briefly introduce yourself, describe the reference table at a high level, and share the available metrics in few sentences.
Then provide 10 numbered example questions in separate lines within a bordered table around all the questions.
At the bottom, you can write that "You may copy from these question examples Or ask new questions related to the data base topic for your prompt".
"""

@st.cache_data(show_spinner="Loading FinnoSQLbot's context...")
def get_table_context(table_name: str, table_description: str, metadata_query: str = None):
    table = table_name.split(".")
    conn = st.connection("snowflake")
    columns = conn.query(f"""
        SELECT COLUMN_NAME, DATA_TYPE FROM {table[0].upper()}.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{table[1].upper()}' AND TABLE_NAME = '{table[2].upper()}'
        """, show_spinner=False,
    )
    columns = "\n".join(
        [
            f"- **{columns['COLUMN_NAME'][i]}**: {columns['DATA_TYPE'][i]}"
            for i in range(len(columns["COLUMN_NAME"]))
        ]
    )
    context = f"""
Here is the table name <tableName> {'.'.join(table)} </tableName>

<tableDescription>{table_description}</tableDescription>

Here are the columns of the {'.'.join(table)}

<columns>\n\n{columns}\n\n</columns>
    """
    if metadata_query:
        metadata = conn.query(metadata_query, show_spinner=False)
        metadata = "\n".join(
            [
                f"- **{metadata['VARIABLE_NAME'][i]}**: {metadata['DEFINITION'][i]}"
                for i in range(len(metadata["VARIABLE_NAME"]))
            ]
        )
        context = context + f"\n\nAvailable variables by VARIABLE_NAME:\n\n{metadata}"
    return context

def welcome_prompt_bot():
    table_context = get_table_context(
        table_name=QUALIFIED_TABLE_NAME,
        table_description=TABLE_DESCRIPTION,
        metadata_query=METADATA_QUERY
    )
    return GEN_SQL.format(context=table_context)

# for the initial welcome prompt by system bot
if __name__ == "__main__":
    st.header("System prompt for FinnoSQLbot")
    st.markdown(welcome_prompt_bot())
