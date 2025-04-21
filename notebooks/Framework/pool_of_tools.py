import bs4
import io
import pandas as pd
import pdfplumber
import importlib
import inspect
from importlib import import_module
import smtplib

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
        data: A dictionary with subject, body, sender, and password.
    Returns:
        Confirmation string
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
@tool
def validate_user(user_id: int, addresses: List[str]) -> bool:
    """
    Validate user using historical addresses.

    Args:
        user_id: The user ID.
        addresses: List of previous addresses.
    """
    return True
     
# --- User validation function ---
@tool
def generate_sql(content: str) -> str:
    """
    Generate Sql script based on content

    Args:
        content: content of sql script
    """
    
    return {"result": f"{content}"}
     




