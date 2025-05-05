# Agent Development Kit (ADK) Crash Course

### Setup Environment

You only need to create one virtual environment for all agent in this course. Follow these steps to set it up:

```bash
# Create virtual environment in the root directory
python -m venv .venv

# Activate (each new terminal)
# macOS/Linux:
source .venv/bin/activate
# Windows CMD:
.venv\Scripts\activate.bat
# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

Once set up, this single environment will work for all examples in the repository.

### Start using

```bash
# cd into development environment
cd ADK

# start adk web to communicate with agent
adk web

# once done
deactivate
```