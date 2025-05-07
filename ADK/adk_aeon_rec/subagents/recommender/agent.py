"""
Recommender Agent

This agent is responsible for recommending promotions
based on various criteria.
"""

from google.adk.agents import Agent
from .prompt import ROOT_AGENT_INSTRUCTION
from .tools import retrieve_basekonwledge  # this auto-registers the tool

#text/csv
# validator_txn_result, validator_demo_result

recommender  = Agent(
    name="recommender",
    model="gemini-2.0-flash",
    description="A bot that make reccomendation based on user demographic and transaction data",
    instruction=ROOT_AGENT_INSTRUCTION,
    tools=[retrieve_basekonwledge.promotions_items],
    output_key="recommender_result"
)

 