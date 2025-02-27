from agents.industry_research_agent import create_industry_research_agent
from agents.use_case_agent import create_use_case_agent
from agents.resource_agent import create_resource_agent
from agents.final_proposal_agent import create_final_proposal_agent
from config import COMPANY_OR_INDUSTRY_TO_RESEARCH

def main():
    """Orchestrates the multi-agent system for market research and use case generation."""

    # 1. Industry Research Agent
    industry_research_agent = create_industry_research_agent()
    print("Running Industry Research Agent...")
    industry_research_output = industry_research_agent.run(industry_or_company=COMPANY_OR_INDUSTRY_TO_RESEARCH)
    print("Industry Research Completed.")

    # 2. Use Case Generation Agent
    use_case_agent = create_use_case_agent()
    print("Running Use Case Generation Agent...")
    use_case_output = use_case_agent.run(industry_research=industry_research_output)
    print("Use Case Generation Completed.")

    # 3. Resource Asset Collection Agent
    resource_agent = create_resource_agent()
    print("Running Resource Collection Agent...")
    resource_output = resource_agent.run(use_cases=use_case_output)
    print("Resource Collection Completed.")

    # 4. Final Proposal Agent
    final_proposal_agent = create_final_proposal_agent()
    print("Running Final Proposal Agent...")
    final_proposal_output = final_proposal_agent.run(
        industry_research=industry_research_output,
        use_cases=use_case_output,
        resource_links=resource_output
    )
    print("Final Proposal Generation Completed.")

    # Save outputs to files
    output_dir = "output"
    import os
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "use_cases.md"), "w") as f:
        f.write(f"# Use Cases for {COMPANY_OR_INDUSTRY_TO_RESEARCH}\n\n")
        f.write(use_case_output)

    with open(os.path.join(output_dir, "resource_links.md"), "w") as f:
        f.write(f"# Resource Links for {COMPANY_OR_INDUSTRY_TO_RESEARCH} Use Cases\n\n")
        f.write(resource_output)

    with open(os.path.join(output_dir, "final_proposal.md"), "w") as f:
        f.write(f"# Final Proposal: AI/GenAI Use Cases for {COMPANY_OR_INDUSTRY_TO_RESEARCH}\n\n")
        f.write(final_proposal_output)


    print("\n--- Final Proposal ---")
    print(final_proposal_output)
    print("\nOutputs saved to the 'output' directory.")


if __name__ == "__main__":
    main()