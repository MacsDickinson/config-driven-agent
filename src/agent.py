from config_agent import load_config, load_tools, load_llm, load_graph
from langchain_core.messages import HumanMessage

# Load configuration
config_model, config_name, config_prompt, config_tools = load_config()

tools = load_tools(config_tools)
llm = load_llm(config_model)
graph = load_graph(config_name, config_prompt, tools, llm)

# Run the graph
response = graph.invoke({"messages": [HumanMessage(content="Hello, how are you?")]})
print(response["messages"][1].content)