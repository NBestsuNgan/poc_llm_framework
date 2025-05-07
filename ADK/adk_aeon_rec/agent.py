"""
Sequential Agent

This Agent do recommendation pipeline with 
perform analyze on user demographic, analyze user transaction data then do recommendation 
"""

from google.adk.agents import SequentialAgent

from .subagents.validator_demo import validator_demo
from .subagents.validator_txn import validator_txn
from .subagents.recommender import recommender

# Create the sequential agent with minimal callback
root_agent = SequentialAgent(
    name="adk_aeon_rec",
    sub_agents=[validator_demo, validator_txn, recommender],
    description="A pipeline that validate user demographic and transaction data and make recommendation",
)