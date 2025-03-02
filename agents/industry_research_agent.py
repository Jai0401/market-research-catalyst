from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
from tools.web_browser import WebBrowserTool
from config import GEMINI_API_KEY, COMPANY_OR_INDUSTRY_TO_RESEARCH

def create_industry_research_agent():
    """Agent to research industry and company information using a web browser tool."""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.2
    )
    
    web_browser_tool = WebBrowserTool()
    
    # Define a list of tools the agent can use.
    tools = [web_browser_tool]
    
    instructions = """
    You are a market research expert. Your goal is to understand a given industry or company.

    1. Identify the industry and its segments.
    2. Outline key offerings and strategic focus areas.

    Use the provided web browser tool when necessary to gather updated and detailed information.

    Industry/Company to Research: {industry_or_company}
    """
    
    prompt_template = PromptTemplate(
        input_variables=["industry_or_company"],
        template=instructions
    )
    
    # Initialize the agent using a zero-shot React-style agent which supports tool calls.
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    
    return agent, prompt_template

