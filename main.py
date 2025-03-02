from agents.industry_research_agent import create_industry_research_agent
from agents.use_case_agent import create_use_case_agent
from agents.resource_agent import create_resource_agent
from agents.final_proposal_agent import create_final_proposal_agent
from config import COMPANY_OR_INDUSTRY_TO_RESEARCH
import os

def main():
    """Orchestrates the multi-agent system for market research and use case generation."""
    
    # 1. Industry Research Agent
    industry_research_agent, industry_research_prompt = create_industry_research_agent()
    print("Running Industry Research Agent...")
    industry_research_query = industry_research_prompt.format(industry_or_company=COMPANY_OR_INDUSTRY_TO_RESEARCH)
    industry_research_output = industry_research_agent.invoke(industry_research_query)
    industry_research_text = (
        industry_research_output.get("output", "") 
        if isinstance(industry_research_output, dict) else industry_research_output
    )
    print("\n--- Industry Research ---")
    print(industry_research_text)
    print("Industry Research Completed.")
    
    # 2. Use Case Generation Agent
    use_case_agent, use_case_prompt = create_use_case_agent()
    print("Running Use Case Generation Agent...")
    use_case_output = use_case_agent.invoke({"industry_research": industry_research_text})
    use_cases_text = use_case_output.content
    print("Use Case Generation Completed.")

    # Save outputs to files
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, "use_cases.md"), "w") as f:
        f.write(use_cases_text)
    
    # 3. Resource Asset Collection Agent
    resource_agent, resource_prompt = create_resource_agent()
    print("Running Resource Collection Agent...")
    resource_query = resource_prompt.format(use_cases=use_cases_text)
    resource_output = resource_agent.invoke(resource_query)
    resource_text = (
        resource_output.get("output", "") 
        if isinstance(resource_output, dict) else resource_output
    )
    print("Resource Collection Completed.")

    with open(os.path.join(output_dir, "resource_links.md"), "w") as f:
        f.write(f"# Resource Links for {COMPANY_OR_INDUSTRY_TO_RESEARCH} Use Cases\n\n")
        f.write(resource_text)
    
    # 4. Final Proposal Agent
    final_proposal_agent, final_proposal_prompt = create_final_proposal_agent()
    print("Running Final Proposal Agent...")
    final_proposal_output = final_proposal_agent.invoke({
        "industry_research": industry_research_text,
        "use_cases": use_cases_text,
        "resource_links": resource_text
    })
    # Extract the text output from the final proposal agent's response.
    final_proposal_text = final_proposal_output.content
    print("Final Proposal Generation Completed.")
    
    with open(os.path.join(output_dir, "final_proposal.md"), "w") as f:
        f.write(final_proposal_text)
    
    print("\n--- Final Proposal ---")
    print("\nOutputs saved to the 'output' directory.")

if __name__ == "__main__":
    main()
