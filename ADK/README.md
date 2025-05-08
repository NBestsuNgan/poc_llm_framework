# Agent & LLM

## Table of Contents
- [Agent Development Kit](#agent-development-kit)


## Agent Development Kit

### Setup Environment

You only need to create one virtual environment for all agent in this folder. Follow these steps to set it up:

```bash
# cd into development environment
cd ADK

# Create virtual environment in the root directory
python -m venv .venv

# Activate 
# macOS/Linux:
source .venv/bin/activate
# Windows CMD:
.venv\Scripts\activate.bat
# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

Once set up, this single environment will work for all examples in the folder.

### Start using

```bash
# start adk web to communicate with agent in web ui
adk web

# stop web ui
ctrl + c

# once done
deactivate
```