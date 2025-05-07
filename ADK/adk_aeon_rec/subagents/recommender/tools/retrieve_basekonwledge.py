import pandas as pd
from typing import List
import os 

# Load your CSV file (replace with your actual path)
base_dir = os.path.dirname(__file__)
# Go to the baseknowledge folder relative to this file
csv_path = os.path.join(base_dir, "..", "baseknowledge", "promotion.csv")

# Load the CSV
df = pd.read_csv(os.path.abspath(csv_path))

def promotions_items() -> List[str]:
    """
    Promotion items from the dataset based on Promotion ID,	Promotion Name,	Category, Eligible Cards, Validity Period, Key Details

    Returns a list of Promotion item .
    """
    data_list = df.to_dict(orient="records")

    # Format nicely for LLM prompt
    formatted_data = "\n".join(
        [f"{i+1}. " + ", ".join([f"{k}: {v}" for k, v in row.items()]) for i, row in enumerate(data_list)]
    )

    return formatted_data  # Limit to top 5 results
