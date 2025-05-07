"""
Validator Demographic Agent

This agent is responsible for analyze user demographic data
"""

from google.adk.agents import Agent
from .prompt import ROOT_AGENT_INSTRUCTION


validator_demo = Agent(
    name="validator_demo",
    model="gemini-2.0-flash",
    description="A bot that analyze user demographic data",
    instruction=ROOT_AGENT_INSTRUCTION,
    output_key="validator_demo_result",
)

