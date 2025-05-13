from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from adk_short_bot.prompt import ROOT_AGENT_INSTRUCTION
from adk_short_bot.tools import count_characters
import platform
import os
from datetime import datetime

# host = "localhost"
# if "linux" in platform.system().lower() and os.path.exists("/.dockerenv"):
#     host = "host.docker.internal"

# OLLAMA_BASE_URL = f"http://{host}:11434"

# ollama_model = LiteLlm(model="ollama_chat/llama3-groq-tool-use:8b", base_url=OLLAMA_BASE_URL)

# print(f"########################################## llama3-groq-tool-use:8b latest update {datetime.now()} ######################################################")

# root_agent = Agent(
#     name = "adk_short_bot",
#     model = ollama_model,
#     description="A bot that shortens messages while maintaining their core meaning",
#     instruction=ROOT_AGENT_INSTRUCTION,
#     tools=[count_characters],
# )

root_agent = Agent(
    name="adk_short_bot",
    model="gemini-2.0-flash",
    description="A bot that shortens messages while maintaining their core meaning",
    instruction=ROOT_AGENT_INSTRUCTION,
    tools=[count_characters],
)
