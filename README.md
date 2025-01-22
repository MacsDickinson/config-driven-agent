# Langchain Agent Config

This is a simple config for a Langchain agent. It is used to configure the agent and its tools.

## Requirements

- Python 3.10+
- Langchain 3.10+
- Langchain Community 3.10+
- Langchain OpenAI 3.10+
- Langchain Anthropic 3.10+
- PyGithub 3.10+
- Atlassian Python API 3.10+

## Setup

1. Clone the repository
   ```bash
   git clone https://github.com/MacsDickinson/langchain-agent-config.git
   ```
2. Create a new virtual environment
   ```bash
   python -m venv .venv
   ```
3. Install the requirements
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the `.env.example` file to `.env` and add your API keys
   ```bash
   cp .env.example .env
   ```
5. Run the agent
   ```bash
   python src/agent.py
   ```

## Run with Langgraph Studio

1. Install Langgraph Studio from [here](https://studio.langchain.com/)
2. Open the root directory of the project

## Notes

- The agent is configured in `src/agent-config.json`
<!-- - The agent is run in `src/main.py` -->
- The agent uses the `langchain-community` library to create the agent and its tools
- The agent uses the `langchain-openai` library to create the OpenAI tools
- The agent uses the `langchain-anthropic` library to create the Anthropic tools
- The agent uses the `pygithub` library to create the GitHub tools
- The agent uses the `atlassian-python-api` library to create the Jira tools
