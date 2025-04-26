import bs4
import io
import pandas as pd
import pdfplumber
import importlib
import inspect
from importlib import import_module
import smtplib
import oracledb

from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.tools import tool

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import Weaviate
from langchain_community.embeddings import OllamaEmbeddings

from langchain_ollama.llms import OllamaLLM

import weaviate
from weaviate.classes.query import MetadataQuery, Filter

import re
from typing_extensions import TypedDict
from typing import List

from email.message import EmailMessage
from Framework import base_tools

# Define tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b


@tool
def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

# --- TypedDict for input schema ---
class EmailInput(TypedDict):
    sender_email: str
    app_password: str
    recipient_email: str
    subject: str
    body: str


# --- Email sending function ---
@tool
def send_google_email(data: dict) -> str:
    """
    Sends an email using Gmail.

    Args:
        data: A dictionary containing:
            - subject (str): The subject line of the email.
            - body (str): The body content of the email.
            - sender_email (str): The sender Gmail address.
            - app_password (str): The Gmail app password (not the regular password).
            - recipient_email (str): The recipient's email address.
    
    Returns:
        str: Confirmation message of email status.
    """
    
    # Inject your actual Gmail credentials (ideally pulled from env vars or a secrets manager)
    data['sender_email'] = data.get('sender_email', 'your_email@gmail.com')
    data['app_password'] = data.get('app_password', 'your_gmail_app_password')
    data['recipient_email'] = data.get('recipient_email', data.get('to'))  # fallback

    # Build and send email
    msg = EmailMessage()
    msg['Subject'] = data['subject']
    msg['From'] = data['sender_email']
    msg['To'] = data['recipient_email']
    msg.set_content(data['body'])
 
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(data['sender_email'], data['app_password'])
            server.send_message(msg)
            print("Email sent successfully!")
            return "Email sent successfully"
    except Exception as e:
        print("Error:", e)
        return str(e)


# --- User validation function ---
# @tool
# def validate_user(user_id: int, addresses: List[str]) -> bool:
#     """
#     Validate user using historical addresses.

#     Args:
#         user_id: The user ID.
#         addresses: List of previous addresses.
#     """
#     return True
    
# @tool
# def list_tables(reasoning: str) -> str:
#     """
#     List all user-created tables in the database (exclude oracle system table).

#     Args:
#         reasoning: Detailed explanation of why you need to see all tables (relate to user's query)

#     Returns:
#         Strign representation of a list containing all tables name
#     """
#     connection = base_tools.register_oracle()
#     cursor = connection.cursor()
#     try:
#         cursor.execute("SELECT owner || '.' || table_name AS table_name FROM all_tables WHERE owner = 'EDP'")
        
#         tables = [row[0] for row in cursor.fetchall()]
#         cursor.close()
#         connection.close()
#         return {"result": f"{str(tables)}"} 
#     except Exception as e:
#         cursor.close()
#         connection.close()
#         return f"Error listing tables: {str(e)}"

    
# @tool
# def sample_table(reasoning: str, table_name: str, row_sample_size: int) -> str:
#     """
#     Retrieves a small sample of rows to understand the data structure and content of a specific table.

#     Args:
#         reasoning: Detailed explanation of why you need to see sample data from this table
#         table_name: Exact name of the table to sample (case-sensitive, no quotes needed)
#         row_sample_size: Number of rows to retrieve (recommended: 3-5 rows for readability)

#     Returns:
#         String with one row per line, showing all columns for each row as tuples
#     """
#     connection = base_tools.register_oracle()
#     cursor = connection.cursor()
#     try:
#         cursor.execute(f"SELECT * FROM {table_name} LIMIT {row_sample_size}")
#         rows = cursor.fetchall()
#         result = '\n'.join([str(row) for row in rows])
#         cursor.close()
#         connection.close()
#         return {"result": f"{result}"} 
#     except Exception as e:
#         cursor.close()
#         connection.close()
#         return f"Error listing tables: {str(e)}"


@tool
def describe_table(reasoning: str, table_name: str) -> str:
    """
    Returns detailed schema information about a table (column, types, constraints).

    Args:
       reasoning: Detailed explanation of why you need to undestand this table's structure
       table_name: Exact name of the table to describe (case-sensitive, no quotes needed)

    Returns:
        String containing table schema information
    """
    connection = base_tools.register_oracle()
    cursor = connection.cursor()
    try:
        return pd.read_sql_query(f"""SELECT c.owner AS SCHEMA,
                                        c.table_name,
                                        c.column_name, 
                                        cc.comments AS column_comment
                                    FROM all_col_comments cc
                                    LEFT JOIN all_tab_columns c
                                    	ON c.owner = cc.owner
                                        AND c.table_name = cc.table_name
                                        AND c.column_name = cc.column_name 
                                    WHERE
                                        c.owner = 'EDP'
                                        AND c.table_name = '{table_name}'
                                    ORDER BY
                                        c.table_name, c.column_id;
        """, connection).to_markdown()
        # rows = cursor.fetchall()
        # result = '\n'.join([str(row) for row in rows])
        # cursor.close()
        # connection.close()
        # return {"result": f"{result}"} 
    except Exception as e:
        # cursor.close()
        connection.close()
        return f"Error listing tables: {str(e)}"


@tool
def execute_sql(reasoning: str, sql_query: str) -> str:
    """
    Execute SQL query and returns the result

    Args:
        reasoning: Explanation of why this query is being run
        sql_query: Complete properly formatted SQL query

    Returns:
        String with query results
   
    """
    connection = base_tools.register_oracle()
    cursor = connection.cursor()
    try:
        return pd.read_sql_query(sql_query, connection).to_markdown()
        # rows = cursor.fetchall()
        # result = '\n'.join([str(row) for row in rows])
        # cursor.close()
        # connection.close()
        # return {"result": f"{result}"} 
    except Exception as e:
        # cursor.close()
        connection.close()
        return f"Error listing tables: {str(e)}"

























