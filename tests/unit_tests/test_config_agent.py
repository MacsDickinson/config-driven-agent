from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from src.config_agent import load_config, load_tools, load_llm

def test_load_config() -> None:
    config_model, config_name, config_prompt, config_tools = load_config("./tests/unit_tests/test-config.json")
    assert config_model == "openai"
    assert config_name == "test assistant"
    assert config_prompt == "You are a test."
    assert config_tools == ["jira", "github"]

def test_load_tools() -> None:
    tools_jira_github = load_tools(["github", "jira"])
    tools_jira = load_tools(["jira"])
    assert len(tools_jira_github) > len(tools_jira)

def test_load_llm_openai() -> None:
    llm = load_llm("openai", [])
    assert isinstance(llm, ChatOpenAI)

def test_load_llm_anthropic() -> None:
    llm = load_llm("anthropic", [])
    assert isinstance(llm, ChatAnthropic)