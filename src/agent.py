import argparse
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from config_agent import load_config, load_tools, load_llm, load_graph
from langchain_core.messages import HumanMessage

# Set up argument parser
parser = argparse.ArgumentParser(description='Run agent with specified config')
parser.add_argument('--character', '-c', 
                    default="./characters/agent-config.json",
                    help='Path to the character config JSON file')

args = parser.parse_args()
config_path = args.character

# Load configuration
config_model, config_name, config_prompt, config_tools = load_config(config_path)

tools = load_tools(config_tools)
llm = load_llm(config_model)
graph = load_graph(config_name, config_prompt, tools, llm)

# Run the graph
response = graph.invoke({"messages": [HumanMessage(content="Hello, how are you?")]})
print(response["messages"][1].content)