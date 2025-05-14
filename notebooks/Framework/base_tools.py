from types import ModuleType
import json
import boto3
from botocore.config import Config
import pandas as pd
from io import StringIO, BytesIO
from pyspark.sql import SparkSession
import pyarrow.parquet as pq
from datetime import datetime
import weaviate
from langchain_core.tools import tool
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from typing_extensions import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from langgraph.graph import MessagesState
from typing import List
import oracledb
import subprocess
from pathlib import Path
import os
import shutil
from botocore.config import Config


    
@staticmethod
def register_datalake():
    """
    Connect to Data Lake Minio

    
    """
    s3 = boto3.client(
        's3',
        endpoint_url='http://minio:9000',  # Replace with your MinIO server URL
        aws_access_key_id='minioadmin',    # Use MinIO's access key
        aws_secret_access_key='minioadmin',# Use MinIO's secret key
        config=Config(signature_version='s3v4')
    )
    return s3


@staticmethod
def register_vecterdb():
    """
    Connect to Vector Database Weaviate

    
    """
    client = weaviate.connect_to_custom(
        http_host="host.docker.internal",
        http_port=8081,
        http_secure=False,
        grpc_host="host.docker.internal",
        grpc_port=50051,
        grpc_secure=False,
    )
    return client

@staticmethod
def register_oracle():
    connection = oracledb.connect(
        user="system",
        password="oracle",
        dsn="host.docker.internal:1521/XEPDB1"
    )        
    return connection

    
@staticmethod
def read_file_from_datalake(bucket_name, path_to_file):
    """
    Read file from Data Lake Minio
    """
    s3 = register_datalake()
    response = s3.get_object(Bucket=bucket_name, Key=path_to_file)
    file_data = response['Body'].read()#.decode('utf-8')
    return file_data

@staticmethod
def upload_fileobj_to_datalake(file, bucket_name, path_to_file):
    """
    Upload file to Data Lake Minio
    """
    s3 = register_datalake()
    s3.upload_fileobj(file, bucket_name, path_to_file)
    
    print(f"UPLOAD FILE TO S3://{bucket_name}/{path_to_file} SUCCESSFULY!")
    
@staticmethod
def upload_filepath_to_datalake(file, bucket_name, path_to_file):
    """
    Upload file to Data Lake Minio
    """
    s3 = register_datalake()
    s3.upload_file(file, bucket_name, path_to_file)
    
    print(f"UPLOAD FILE TO S3://{bucket_name}/{path_to_file} SUCCESSFULY!")
 


@staticmethod
def register_agent(agent_path: str):
    ADK_SOURCE_DIR = agent_path #/ADK/PKG_NAME 
    ADK_TARGET_DIR = 'packaged_agent/' + agent_path #/packaged_agentADK/PKG_NAME 
    PKG_NAME = agent_path.split('/')[1] #PKG_NAME 
    
    # Step 1: Copy source folder to a clean new target location
    SOURCE_DIR = Path("/tmp") / Path(ADK_SOURCE_DIR)
    TARGET_DIR = Path("/tmp") / Path(ADK_TARGET_DIR)
    
    print("SOURCE_DIR :", SOURCE_DIR)
    print("TARGET_DIR :", TARGET_DIR)
    
    #remove .env file
    # def ignore_dotfiles(dir, files):
    #     return [f for f in files if f.startswith('.')]
    
    # Remove TARGET_DIR if it already exists
    if TARGET_DIR.exists():
        shutil.rmtree(TARGET_DIR)
    shutil.copytree(SOURCE_DIR, TARGET_DIR) #ignore=ignore_dotfiles
    
    # Step 2: Restructure into proper Python package
    PKG_DIR = TARGET_DIR / PKG_NAME
    DIST_DIR = TARGET_DIR / "dist"
    
    # Step 1: Move Python files into PKG_NAME / subfolder
    if not PKG_DIR.exists():
        PKG_DIR.mkdir()
        for file in TARGET_DIR.glob("*.py"):
            if file.name != "setup.py":
                shutil.move(str(file), str(PKG_DIR / file.name))
    
    # Step 2: Move folders (like 'tools') into the package dir
    for sub in TARGET_DIR.iterdir():
        if sub.is_dir() and sub.name != PKG_NAME and sub.name != "dist":
            shutil.move(str(sub), str(PKG_DIR / sub.name))
    
    # Step 3: Ensure __init__.py exists
    (PKG_DIR / "__init__.py").touch(exist_ok=True)
    
    # Step 4: Write or overwrite setup.py
    setup_code = f"""
from setuptools import setup, find_packages

setup(
    name="{PKG_NAME}",
    version="0.1.0",
    description="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "google-cloud-aiplatform[adk,agent_engines]",
    ],
    python_requires=">=3.8",
)
"""
    with open(TARGET_DIR / "setup.py", "w") as f:
        f.write(setup_code)
    
    # Step 5: Build and install the package
    subprocess.run(["python", "-m", "build", "--outdir", str(DIST_DIR)], cwd=TARGET_DIR, check=True)
    subprocess.run(["pip", "install", str(list(DIST_DIR.glob("*.whl"))[0])], check=True)

    for fpath in DIST_DIR.glob("*"):
        key = f"{PKG_NAME}/{fpath.name}"    
        upload_filepath_to_datalake(str(fpath), 'datalake', f'Agent/{key}')
        
        print(f"☁️ Uploaded {fpath.name} to s3://datalake/Agent/{key}")

    # MINIO_KEY = f"Agent/{PKG_NAME}/{PKG_NAME}-0.1.0-py3-none-any.whl" 
    MINIO_KEY = f"Agent/{PKG_NAME}/{PKG_NAME}-0.1.0.tar.gz"
    LOCAL_PKG_PATH = Path("/tmp/registered_agent") / Path(MINIO_KEY).name
    
    print("MINIO_KEY :", MINIO_KEY)
    print("LOCAL_PKG_PATH :", LOCAL_PKG_PATH)
    
    # === Ensure download directory exists ===
    LOCAL_PKG_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # === Download from MinIO ===
    s3 = register_datalake()
    
    print(f"⬇️  Downloading {MINIO_KEY} from MinIO...")
    s3.download_file("datalake", MINIO_KEY, str(LOCAL_PKG_PATH))
    print(f"✅ Downloaded to: {LOCAL_PKG_PATH}")
    
    # === Uninstall package if found ===
    print(f"⛔ Uninstalling any existing versions of {PKG_NAME}...")
    subprocess.run(["pip", "uninstall", PKG_NAME, "-y"], check=False)
    
    # === Install package === persistence as long as container don't force to shutdown
    print(f"📦 Installing {LOCAL_PKG_PATH.name}...")
    subprocess.run(["pip", "install", str(LOCAL_PKG_PATH)], check=True)
    print("✅ Package installed.")
    print("##############################################################################################\n\n")




@staticmethod
def get_table_info(query: str) -> str:
    """
    Execute SQL query to returns demographic infomation of user.
    """
    connection = register_oracle()
    try:
        return pd.read_sql_query(query, connection)
    except Exception as e:
        connection.close()
        return f"Error listing tables: {str(e)}"

@staticmethod
def write_to_oracle(table_name, df):
    import re

    # Optional: sanitize column names
    def quote_column(col):
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", col):
            return f'"{col}"'
        return col

    columns = [quote_column(col) for col in df.columns]

    # Prepare data for insertion
    data_as_tuples = [tuple(row) for row in df.itertuples(index=False, name=None)]

    connection = register_oracle()
    oc = connection.cursor()

    placeholders = ", ".join([f":{i+1}" for i in range(len(columns))])
    insert_sql = f"INSERT INTO EDP.{table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    try:
        oc.executemany(insert_sql, data_as_tuples)
        connection.commit()
        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")
        connection.rollback()
        raise
    finally:
        oc.close()
        connection.close()


 