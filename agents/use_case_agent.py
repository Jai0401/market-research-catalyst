from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
from tools.web_browser import WebBrowserTool
from config import GEMINI_API_KEY

def create_use_case_agent():
    """Agent to generate relevant AI/GenAI use cases based on industry research."""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.2
    )


    web_browser_tool = WebBrowserTool()

    # Define a list of tools the agent can use.
    tools = [web_browser_tool]

    prompt_template = PromptTemplate(
        input_variables=["industry_research"],
        template="""
        You are an AI and Generative AI use case generation expert.
        Based on the provided industry research, analyze industry trends and standards related to AI, ML, and automation in this sector.

        Industry Research:
        {industry_research}

        Propose relevant use cases where the company or industry can leverage GenAI, LLMs, and ML technologies to improve their processes, enhance customer satisfaction, and boost operational efficiency.
        Focus on practical and impactful use cases. Consider areas like:
        - Operations Enhancement
        - Customer Experience Improvement
        - Automation of tasks
        - New product/service opportunities

        For each use case, briefly explain:
        - The use case itself.
        - How GenAI/ML can be applied.
        - Potential benefits for the company/industry.
        
        Use the provided web browser tool when necessary to gather updated and detailed information.
        List at least 5 use cases. Add references or sources if you know of any similar implementations in the industry.
        """
    )

        # Initialize the agent using a zero-shot React-style agent which supports tool calls.
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    return agent, prompt_template

