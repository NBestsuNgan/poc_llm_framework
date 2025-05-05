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
def get_user_demographic() -> str:
    """
    Execute SQL query to returns demographic infomation of user.
    """
    connection = register_oracle()
    try:
        return pd.read_sql_query("""
                    SELECT demo.*, 
                           pc.period, 
                           pc.latest_promotion_cr, 
                           rt.latest_reward_type, 
                           sdc.latest_shopping_discount_cr
                    FROM EDP.DEMOGRAPHIC demo
                    LEFT JOIN EDP.PROMTION_CR pc 
                        ON demo.aeon_id = pc.aeon_id 
                    LEFT JOIN EDP.REWARD_TYPE rt 
                        ON demo.aeon_id = rt.aeon_id 
                        AND pc.period = rt.period
                    LEFT JOIN EDP.SHOPPING_DISCOUNT_CR sdc
                        ON demo.aeon_id = sdc.aeon_id 
                        AND pc.period = sdc.period
                """, connection)
    except Exception as e:
        connection.close()
        return f"Error listing tables: {str(e)}"

@staticmethod
def get_table_description() -> str:
    """
    Execute SQL query to returns demographic infomation of user.
    """
    connection = register_oracle()
    try:
        return pd.read_sql_query("""
                    WITH main1 AS (
                        SELECT
                            c.owner || '.' || c.table_name AS TABLE_NAME,
                            t.comments AS table_comment
                        FROM
                            all_tab_columns c
                        LEFT JOIN
                            all_col_comments col
                            ON c.owner = col.owner
                            AND c.table_name = col.table_name
                            AND c.column_name = col.column_name
                        LEFT JOIN
                            all_tab_comments t
                            ON c.owner = t.owner
                            AND c.table_name = t.table_name
                        WHERE
                            c.owner = 'EDP'
                    )
                    SELECT DISTINCT * FROM main1
                    ORDER BY table_name
                """, connection).to_markdown()
    except Exception as e:
        connection.close()
        return f"Error listing tables: {str(e)}"


@staticmethod
def get_table_info(query: str) -> str:
    """
    Execute SQL query to returns demographic infomation of user.
    """
    connection = register_oracle()
    try:
        return pd.read_sql_query(query, connection).to_markdown()
    except Exception as e:
        connection.close()
        return f"Error listing tables: {str(e)}"
