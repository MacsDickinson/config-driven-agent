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
6. Run the agent with a specific character
   ```bash
   python src/agent.py --character characters/agent-sunny.json
   ```

### Running the github tool

In order to run the github tool you need to set the following environment variables:

- `GITHUB_APP_ID`: The id of the github app - generate this by creating a new github app [here](https://github.com/settings/apps/new)
- `GITHUB_APP_PRIVATE_KEY`: The path to the private key of the github app - generate this from your newly created github app
- `GITHUB_REPOSITORY`: The name of the repository to use

### Running the jira tool

In order to run the jira tool you need to set the following environment variables:

- `JIRA_API_TOKEN`: The api token of the jira account - generate this from your jira account
- `JIRA_USERNAME`: The username of the jira account
- `JIRA_INSTANCE_URL`: The url of the jira instance
- `JIRA_CLOUD`: Whether the jira instance is cloud or not

### Running the slackbot

In order to run the slackbot you need to set the following environment variables:

- `SLACK_BOT_TOKEN`: The token of the slack bot
- `SLACK_APP_TOKEN`: The token of the slack app
- `SLACK_SIGNING_SECRET`: The signing secret of the slack app

Run the slackbot with the following command:

```bash
python src/slackbot.py
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
