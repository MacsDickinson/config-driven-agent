import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from config_agent import load_config, load_tools, load_llm, load_graph
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables from .env file
load_dotenv()

# Initialize the Slack app
app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

# Initialize the agent
config_model, config_name, config_prompt, config_tools = load_config("./characters/agent-sunny.json")

tools = load_tools(config_tools)
llm = load_llm(config_model)
graph = load_graph(config_name, config_prompt, tools, llm)


def respond_to_thread(messages, event, say):
    for message in messages:
        say(message, thread_ts=event.get("thread_ts", None) or event["ts"])
    
def get_llm_response(body):
    event = body["event"]
    response = graph.invoke({"messages": [HumanMessage(content=event['text'])]})
    return [msg.content for msg in response["messages"] if isinstance(msg, AIMessage) and msg.content]

@app.event("message")
def handle_message_events(body, say, client):
    event = body['event']
    bot_id = body['authorizations'][0]['user_id']
    
    # reply if this is a DM
    if event['channel_type'] == "im":
        respond_to_thread(get_llm_response(body), event, say)
    elif 'thread_ts' in event:
        # Get the parent message
        result = client.conversations_replies(
            channel=event['channel'],
            ts=event['thread_ts'],
            limit=1
        )
        if result['messages']:
            parent_message = result['messages'][0]
            # Check if the parent message mentions the bot
            if f"<@{bot_id}>" in parent_message['text']:
                respond_to_thread(get_llm_response(body), event, say)
                

@app.event("app_mention")
def handle_app_mention(body, say):
    respond_to_thread(get_llm_response(body), body['event'], say)

# Start the app
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))
    handler.start()
