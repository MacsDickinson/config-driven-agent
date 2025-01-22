from src.config_agent import load_config, load_tools, load_llm, load_graph

# Load configuration
config_model, config_name, config_prompt, config_tools = load_config()

tools = load_tools(config_tools)
llm = load_llm(config_model)
graph = load_graph(config_name, config_prompt, tools, llm)