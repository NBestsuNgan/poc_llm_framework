from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from adk_short_bot.prompt import ROOT_AGENT_INSTRUCTION
from adk_short_bot.tools import count_characters


ollama_model = LiteLlm(model="ollama_chat/qwen2.5:7b")


root_agent = Agent(
    name = "adk_short_bot",
    model = ollama_model,
    description="A bot that shortens messages while maintaining their core meaning",
    instruction=ROOT_AGENT_INSTRUCTION,
    tools=[count_characters],
)

# root_agent = Agent(
#     name="adk_short_bot",
#     model="gemini-2.0-flash",
#     description="A bot that shortens messages while maintaining their core meaning",
#     instruction=ROOT_AGENT_INSTRUCTION,
#     tools=[count_characters],
# )
