from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import GEMINI_API_KEY, COMPANY_OR_INDUSTRY_TO_RESEARCH

def create_final_proposal_agent():
    """Agent to create the final proposal, summarizing use cases and resources."""
    
    # Initialize the LLM using your Gemini API key.
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.2
    )

    # Define the prompt template with the necessary placeholders.
    prompt_template = PromptTemplate(
        input_variables=["industry_research", "use_cases", "resource_links", "company_name"],
        template="""
        You are a final proposal generation expert.
        Based on the industry research, generated use cases, and collected resource links, create a final proposal document specifically for {company_name}.

        Industry Research:
        {industry_research}

        Generated Use Cases:
        {use_cases}

        Resource Links:
        {resource_links}

        Your tasks are:
        1. **Summarize the top use cases** (prioritize based on relevance and impact). Select the top 3-5 most impactful use cases specifically for {company_name}.
        2. **Ensure Relevance:** Confirm that the selected use cases are directly relevant to {company_name}'s goals and operational needs based on the industry research.
        3. **Add References:** Include any references or sources that were used to suggest these use cases (from the research or use case generation steps).
        4. **Format for Proposal:** Structure the output as a clear and concise proposal document. Include clickable resource links where applicable (especially for datasets).

        Structure of the proposal should be:
        - **Title:** AI/GenAI Strategic Proposal for {company_name} (use this exact format)
        - **Introduction:** Briefly introduce the purpose of the proposal, specifically highlighting how AI/GenAI can benefit {company_name}.
        - **{company_name} Overview:** Summarize key findings about {company_name} from the industry research.
        - **Top Use Case Proposals for {company_name}:** Detail each top use case, including benefits and potential implementation strategies.
        - **Resource Assets:** List relevant dataset and resource links for each use case.
        - **Conclusion:** Summarize the value proposition and next steps for {company_name}.
        
        Ensure the company name {company_name} is prominently featured throughout the document and highlighted in bold at key points only.
        """
    )

    # Create the chain without any external tools.
    final_proposal_chain = prompt_template | llm
    return final_proposal_chain, prompt_template

