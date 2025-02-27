from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from config import GEMINI_API_KEY
from tools.web_browser import WebBrowserTool

def create_resource_agent():
    """Agent to collect relevant datasets and resources for the generated use cases."""

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.2
    )
    web_browser_tool = WebBrowserTool()

    prompt_template = PromptTemplate(
        input_variables=["use_cases"],
        template="""
        You are a resource finding expert, specializing in datasets and AI/ML resources.
        For the following AI/GenAI use cases, search for relevant datasets on platforms like Kaggle, HuggingFace Datasets, and GitHub.
        Also, look for any relevant articles, blog posts, or open-source projects that could be helpful for implementing these use cases.

        Use Cases:
        {use_cases}

        For each use case, find at least one relevant dataset link and any other helpful resource links.
        Provide a list of use cases with corresponding resource links.  Make sure the links are clickable.

        Example Output Format:
        Use Case 1: [Use Case Description]
        - Dataset Link 1: [Link to Dataset 1]
        - Resource Link 1: [Link to Resource 1]
        - Resource Link 2: [Link to Resource 2]

        Use Case 2: [Use Case Description]
        - ... (and so on for each use case)
        """
    )

    resource_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="resource_links")
    return resource_chain

if __name__ == '__main__':
    # Example Usage (you'd get use_cases from the use_case_agent)
    example_use_cases = """
    Use Case 1: Predictive Maintenance in Manufacturing
    Use Case 2: AI-Powered Customer Service Chatbot for Automotive Dealers
    """
    resource_agent = create_resource_agent()
    resource_links = resource_agent.run(use_cases=example_use_cases)
    print("Resource Links:")
    print(resource_links)