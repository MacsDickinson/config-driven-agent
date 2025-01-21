# Load config
import json
from langchain_core.messages import SystemMessage

from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

def sanitise_tools_functions(tools):
    """
    Sanitise the names of the tools and their functions so they play nicely with the LLM.
    """
    import re
    for tool in tools:    
        sanitized_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', tool.name)
        tool.name = sanitized_name
        if hasattr(tool, "func"):
            tool.func.__name__ = sanitized_name

    return tools

def load_tools(config_tools):
    """
    Load tools based on configuration settings.
    
    Args:
        config_tools (list): List of tool names to load
        
    Returns:
        list: List of initialized tools
    """
    tools = []

    # only add github if specified in tools array
    if "github" in config_tools:
        from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
        from langchain_community.utilities.github import GitHubAPIWrapper

        github = GitHubAPIWrapper()
        toolkit = GitHubToolkit.from_github_api_wrapper(github)
        tools = tools + toolkit.get_tools()

    # add jira if specified in tools array
    if "jira" in config_tools:
        from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit
        from langchain_community.utilities.jira import JiraAPIWrapper

        jira = JiraAPIWrapper()
        toolkit = JiraToolkit.from_jira_api_wrapper(jira)
        tools = tools + toolkit.get_tools()

    return sanitise_tools_functions(tools)

def load_config(config_path="agent-config.json"):
    """
    Load and parse the agent configuration file.
    
    Args:
        config_path (str): Path to the configuration file
        
    Returns:
        tuple: (model, name, prompt, tools) configuration values
    """
    with open(config_path, "r") as f:
        config = json.load(f)
    
    return (
        config.get("model", "openai"),
        config.get("name", "assistant"),
        config.get("prompt", "You are a helpful assistant."),
        config.get("tools", [])
    )

def load_llm(config_model):
    """
    Load the LLM based on the configuration settings.
    """
    # select the model based on what is set in the config
    if config_model == "openai":
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o")
    elif config_model == "anthropic":
        from langchain_anthropic import ChatAnthropic
        llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    else:
        raise ValueError(f"Model {config_model} not supported")

    return llm.bind_tools(tools)


def load_graph(config_name, tools, llm):
    """
    Load the graph based on the configuration settings.
    """
    sys_msg = SystemMessage(content=config_prompt)

    def assistant(state: MessagesState):
        return {"messages": [llm.invoke([sys_msg] + state["messages"])]}

    builder = StateGraph(MessagesState)
    builder.add_node(config_name, assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, config_name)
    builder.add_conditional_edges(
        config_name,
        tools_condition,
    )
    builder.add_edge("tools", config_name)

    return builder.compile()

# Load configuration
config_model, config_name, config_prompt, config_tools = load_config()

tools = load_tools(config_tools)
llm = load_llm(config_model)
graph = load_graph(config_name, tools, llm)