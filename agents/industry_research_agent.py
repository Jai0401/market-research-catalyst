from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from tools.web_browser import WebBrowserTool
from config import GEMINI_API_KEY, COMPANY_OR_INDUSTRY_TO_RESEARCH

def create_industry_research_agent():
    """Agent to research industry and company information."""

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.2
    )
    web_browser_tool = WebBrowserTool()

    prompt_template = PromptTemplate(
        input_variables=["industry_or_company"],
        template="""
        You are a market research expert. Your goal is to understand a given industry or company.

        1. **Identify the industry and segment:** Determine the industry and specific segments the company operates in (e.g., Automotive, Manufacturing, Finance, Retail, Healthcare).
        2. **Key Offerings & Strategic Focus:** Identify the company's key product/service offerings and strategic focus areas (operations, supply chain, customer experience, etc.). Understand their vision and product information.

        Use the web browser tool to research "{industry_or_company}".

        Provide a detailed summary of your findings, focusing on the above points.

        Industry/Company to Research: {industry_or_company}
        """
    )

    research_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="industry_research")

    return research_chain

if __name__ == '__main__':
    research_agent = create_industry_research_agent()
    industry_info = research_agent.run(industry_or_company=COMPANY_OR_INDUSTRY_TO_RESEARCH)
    print("Industry Research Results:")
    print(industry_info)