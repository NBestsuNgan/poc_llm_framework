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


    
@tool
def connect_to_datalake():
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


@tool
def connect_to_vecterdb():
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

@tool
def read_file_from_datalake(bucket_name, path_to_file):
    """
    Read file from Data Lake Minio

    
    """
    s3 = Utility.register_catalog()
    response = s3.get_object(Bucket=bucket_name, Key=path_to_file)
    file_data = response['Body'].read()#.decode('utf-8')
    return file_data

@tool
def af_write_to_oracle(table_name, df):
    """
    Upsert data to Sql Database Oracle

    
    """
    data_to_insert = df.collect()  
    columns = df.columns  
    
    connection = Utility.register_oracle()  
    oc = connection.cursor()
    
    placeholders = ", ".join([f":{i+1}" for i in range(len(columns))])
    insert_sql = f"INSERT INTO EDP.{table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    data_as_tuples = [tuple(row) for row in data_to_insert]
    
    try:
        oc.executemany(insert_sql, data_as_tuples)
        connection.commit()
        print("Data inserted successfully!")
        oc.close()
        connection.close()
    except Exception as e:
        raise(f"Error occurred: {e}")

@tool
def af_execute_to_oracle(bucket_name, script_path):
    """
    Execute sql script in Sql Database Oracle

    
    """
    connection = Utility.register_oracle()  
    oc = connection.cursor()

    s3 = Utility.register_catalog()
    response = s3.get_object(Bucket=bucket_name, Key=script_path)
    script = response['Body'].read().decode('utf-8')
    try:
        statements = script.strip().split(';')
        for stmt in statements:
            if stmt.strip():  # Skip empty statements
                print(f"Executing statement:\n{stmt.strip()}\n")
                oc.execute(stmt.strip())
        
        # Commit changes to the database
        connection.commit()

        oc.close()
        connection.close()
        print("Execution Successful")
    except Exception as e:
        print(f"Error executing script: {e}")





