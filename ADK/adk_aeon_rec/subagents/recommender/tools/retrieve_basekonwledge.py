import pandas as pd
from typing import List
import os 
import oracledb
import platform

# # Load your CSV file (replace with your actual path)
# base_dir = os.path.dirname(__file__)
# # Go to the baseknowledge folder relative to this file
# csv_path = os.path.join(base_dir, "..", "baseknowledge", "promotion.csv")

# # Load the CSV
# df = pd.read_csv(os.path.abspath(csv_path))


def get_oracle_connection():
    # Detect if running inside Docker or on local Windows/macOS
    host = "localhost"
    if "linux" in platform.system().lower() and os.path.exists("/.dockerenv"):
        host = "host.docker.internal"

    dsn = f"{host}:1521/XEPDB1"
    
    connection = oracledb.connect(
        user="system",
        password="oracle",
        dsn=dsn,
    )
    return connection


def promotions_items() -> List[str]:
    """
    Promotion items from the dataset based on Promotion ID,	Promotion Name,	Category, Eligible Cards, Validity Period, Key Details

    Returns a list of Promotion item .
    """
    # data_list = df.to_dict(orient="records")

    connection = get_oracle_connection()

    try:
        df = pd.read_sql_query("""SELECT * FROM EDP.PROMOTIONS""", connection)
    except Exception as e:
        connection.close()
        return f"Error listing tables: {str(e)}"

    data_list = df.to_dict(orient="records")

    # Format nicely for LLM prompt
    formatted_data = "\n".join(
        [f"{i+1}. " + ", ".join([f"{k}: {v}" for k, v in row.items()]) for i, row in enumerate(data_list)]
    )

    return formatted_data  
