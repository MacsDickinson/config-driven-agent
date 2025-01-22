# Langchain Agent Config

This is a simple config for a Langchain agent. It is used to configure the agent and its tools.

## Requirements

- Python 3.10+

## Setup

1. Clone the repository
   ```bash
   git clone https://github.com/MacsDickinson/langchain-agent-config.git
   cd langchain-agent-config
   ```
2. Create a new virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate
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

- The agent is configured in `characters/agent-config.json`
- The agent is run in `src/agent.py`
- The agent uses the `langchain-community` library to create the agent and its tools
- The agent uses the `langchain-openai` library to integrate with OpenAI gpt-4o
- The agent uses the `langchain-anthropic` library to integrate with Anthropic claude-3-5-sonnet
- The agent uses the `pygithub` library to create the GitHub tools
- The agent uses the `atlassian-python-api` library to create the Jira tools
