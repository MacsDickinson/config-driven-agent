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

def load_config(config_path):
    """
    Load and parse the agent configuration file.
    
    Args:
        config_path (str): Path to the configuration file
        
    Returns:
        tuple: (model, name, prompt, tools) configuration values
    """
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}
        
    return (
        config.get("model", "openai"),
        config.get("name", "assistant"),
        config.get("prompt", "You are a helpful assistant."),
        config.get("tools", [])
    )

def load_llm(model):
    """
    Load the LLM based on the configuration settings.
    """
    # select the model based on what is set in the config
    if model == "openai":
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o")
    elif model == "anthropic":
        from langchain_anthropic import ChatAnthropic
        llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    else:
        raise ValueError(f"Model {model} not supported")

    return llm

def load_graph(name, prompt, tools, llm):
    """
    Load the graph based on the configuration settings.
    """
    llm_with_tools = llm if not tools else llm.bind_tools(tools)
    sys_msg = SystemMessage(content=prompt)

    def assistant(state: MessagesState):
        return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

    builder = StateGraph(MessagesState)
    builder.add_node(name, assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, name)
    builder.add_conditional_edges(
        name,
        tools_condition,
    )
    builder.add_edge("tools", name)

    return builder.compile()