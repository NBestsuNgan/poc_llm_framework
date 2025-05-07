"""
Validator transaction Agent

This agent is responsible for analyze user transaction data
"""

from google.adk.agents import Agent
from .prompt import ROOT_AGENT_INSTRUCTION

    

validator_txn = Agent(
    name="validator_txn",
    model="gemini-2.0-flash",
    description="A bot that analyze user transaction data",
    instruction=ROOT_AGENT_INSTRUCTION,
    output_key="validator_txn_result",
    
)

