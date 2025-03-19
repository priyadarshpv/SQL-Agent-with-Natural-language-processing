import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import mysql.connector
import pandas as pd
import re
import sqlparse

# Load environment variables
load_dotenv()

def connect_to_mysql():
    """
    Connects to the MySQL database and returns the connection object.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        print("Connected to MySQL successfully!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

@tool
def execute_sql_query(sql_query: str) -> str:
    """
    Executes a SQL query on the MySQL database and returns the result.
    """
    connection = connect_to_mysql()
    if connection is None:
        return "Failed to connect to MySQL."

    cursor = connection.cursor()
    try:
        cursor.execute(sql_query)
        if sql_query.strip().lower().startswith("select"):
            # Fetch results for SELECT queries
            result = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            return df.to_string()
        else:
            # For INSERT, UPDATE, DELETE queries
            connection.commit()
            return "Query executed successfully."
    except Exception as e:
        return f"Error executing query: {e}"
    finally:
        cursor.close()
        connection.close()

# Initialize Groq LLM
groq_llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="mixtral-8x7b-32768")

# Prompt template for SQL generation
prompt_template = PromptTemplate(
    input_variables=["prompt", "table_name", "columns"],
    template="""
    You are a SQL expert. Given the following natural language input, generate a SQL query to perform the task.

    Rules:
    - Use only the columns provided.
    - Do not include any invalid SQL syntax.
    - Use proper SQL keywords (e.g., SELECT, FROM, WHERE).

    Natural Language Input: {prompt}

    The table name is '{table_name}' and the columns are: {columns}.

    Return only the SQL query, nothing else.

    Note: The natural language input will not be with the correct case, so try lower, upper, capitalized for query if needed.
    """
)

# Initialize LLMChain for SQL generation
sql_chain = LLMChain(llm=groq_llm, prompt=prompt_template)

# Define tools for the agent
tools = [
    Tool(
        name="Execute SQL Query",
        func=execute_sql_query,
        description="Executes a SQL query on the MySQL database and returns the result."
    )
]

# Initialize the agent
agent = initialize_agent(tools, groq_llm, agent="zero-shot-react-description", verbose=True)

def is_valid_sql_query(sql_query):
    """
    Validates if the generated SQL query is syntactically correct.
    """
    try:
        parsed = sqlparse.parse(sql_query)
        if not parsed:
            return False
        return True
    except Exception as e:
        print(f"Error validating SQL query: {e}")
        return False

def main():
    """
    Main function to run the SQL Agent.
    """
    table_name = input("Enter the table name: ")
    prompt = input("Enter your query in natural language: ")

    connection = connect_to_mysql()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        cursor.execute(f"SHOW COLUMNS FROM {table_name};")
        columns = [row[0] for row in cursor.fetchall()]
    except mysql.connector.Error as err:
        print(f"Error fetching columns: {err}")
        return
    finally:
        cursor.close()
        connection.close()

    columns_str = ', '.join(columns)

    # Generate SQL query
    response = sql_chain.invoke({
        "prompt": prompt,
        "table_name": table_name,
        "columns": columns_str
    })
    sql_query = response["text"].replace("\\*", "*")
    print(f"Generated SQL Query: {sql_query}")

    # Validate SQL query
    if not is_valid_sql_query(sql_query):
        print("Error: Invalid SQL query generated.")
        return

    # Execute SQL query
    result = agent.invoke({
        "input": f"Execute the following SQL query: {sql_query}"
    })
    print("Query Result:")
    print(result)

if __name__ == "__main__":
    main()
