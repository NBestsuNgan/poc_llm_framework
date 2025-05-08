from google.adk.agents import Agent

from adk_fuzzy_match_bot.prompt import ROOT_AGENT_INSTRUCTION
from .tools import retrieve_knowledge  # this auto-registers the tool



root_agent = Agent(
    name="adk_fuzzy_match_bot",
    model="gemini-2.0-flash",
    description="A bot that find a similarity word from input message",
    instruction=ROOT_AGENT_INSTRUCTION,
    tools=[retrieve_knowledge.get_datasource],
)
