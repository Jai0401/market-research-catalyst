from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
from tools.web_browser import WebBrowserTool
from config import GEMINI_API_KEY

def create_resource_agent():
    """Agent to collect relevant datasets and resources for the generated use cases."""
    
    # Initialize the LLM using your Gemini API key.
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.2
    )
    
    # Create an instance of the web browser tool.
    web_browser_tool = WebBrowserTool()
    
    # Define the instructions for the resource agent.
    instructions = """
    You are a resource finding expert, specializing in datasets and AI/ML resources.
    For the following AI/GenAI use cases, search for relevant datasets on platforms like Kaggle, HuggingFace Datasets, and GitHub.
    Also, look for any relevant articles, blog posts, or open-source projects that could be helpful for implementing these use cases.

    Use Cases:
    {use_cases}

    For each use case, find at least one relevant dataset link and any other helpful resource links.
    Provide a list of use cases with corresponding resource links. Make sure the links are clickable.

    Example Output Format:
    Use Case 1: [Use Case Description]
    - Dataset Link 1: [Link to Dataset 1]
    - Resource Link 1: [Link to Resource 1]
    - Resource Link 2: [Link to Resource 2]

    Use Case 2: [Use Case Description]
    - ... (and so on for each use case)
    """
    
    prompt_template = PromptTemplate(
        input_variables=["use_cases"],
        template=instructions
    )
    
    # Set up the agent with the web browser tool.
    tools = [web_browser_tool]
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )
    
    # Return both the agent and the prompt template.
    return agent, prompt_template

