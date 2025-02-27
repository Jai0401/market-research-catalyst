from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from config import GEMINI_API_KEY

def create_use_case_agent():
    """Agent to generate relevant AI/GenAI use cases based on industry research."""

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.2
    )

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

        List at least 5 use cases. Add references or sources if you know of any similar implementations in the industry.
        """
    )

    use_case_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="use_cases")
    return use_case_chain

if __name__ == '__main__':
    # Example usage (you'd normally get industry_research from the previous agent)
    example_industry_research = """
    The Automotive Industry is undergoing a massive transformation... (imagine detailed research output here) ... focusing on electric vehicles, autonomous driving, and connected car technologies.
    """
    use_case_agent = create_use_case_agent()
    use_cases = use_case_agent.run(industry_research=example_industry_research)
    print("Generated Use Cases:")
    print(use_cases)