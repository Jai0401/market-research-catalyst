import streamlit as st
import os
import time
from config import COMPANY_OR_INDUSTRY_TO_RESEARCH
import importlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Set page configuration
st.set_page_config(
    page_title="Market Research AI",
    page_icon="📊",
    layout="wide"
)

# App title and description
st.title("Market Research AI")
st.markdown("Generate comprehensive market research and proposal documents using AI")

# Sidebar for input and controls
with st.sidebar:
    st.header("Research Configuration")
    
    # Company/Industry input
    company_name = st.text_input(
        "Enter company or industry to research:", 
        value=COMPANY_OR_INDUSTRY_TO_RESEARCH
    )
    
    # Optional advanced settings
    with st.expander("Advanced Settings"):
        st.caption("API Keys are loaded from .env file by default")
        gemini_api_key = st.text_input("Gemini API Key:", type="password")
        exa_api_key = st.text_input("Exa API Key:", type="password")
    
    # Run button
    run_research = st.button("Generate Research", type="primary")
    
    # Information section
    st.info(
        "This process may take 5-10 minutes to complete as it " 
        "conducts thorough research across multiple sources."
    )

# Add to sidebar
with st.sidebar:
    st.header("Research History")
    
    # List files in output directory
    previous_research = []
    if os.path.exists("output"):
        for file in os.listdir("output"):
            if file.endswith("_proposal.md"):
                previous_research.append(file.replace("_proposal.md", ""))
    
    if previous_research:
        selected_previous = st.selectbox("View previous research:", previous_research)
        if st.button("Load Selected Research"):
            # Logic to load previous research
            pass
    else:
        st.text("No previous research found.")

# Add to sidebar
with st.sidebar:
    st.header("Comparative Analysis")
    competitor = st.text_input("Compare with competitor (optional):")
    if competitor and st.button("Run Comparison"):
        # Logic to run competitor analysis
        pass

# Main content area
if not run_research:
    # Display welcome screen with instructions
    st.markdown("""
    ## Welcome to Market Research AI
    
    This tool automates the process of market research and proposal creation using AI.
    
    ### How it works:
    1. Enter a company or industry name in the sidebar
    2. Click "Generate Research"
    3. The AI will:
       - Research the company/industry
       - Generate relevant use cases
       - Find supporting resources
       - Create a comprehensive proposal
    
    ### Example companies to try:
    - Scale AI
    - Snowflake
    - Electric Vehicles Industry
    - Healthcare AI
    """)

else:
    # Update the company name in config
    import config
    config.COMPANY_OR_INDUSTRY_TO_RESEARCH = company_name
    
    # Set API keys if provided
    if gemini_api_key:
        config.GEMINI_API_KEY = gemini_api_key
    if exa_api_key:
        config.EXA_API_KEY = exa_api_key
    
    # Reset module to apply config changes
    importlib.reload(config)
    
    # Set up progress tracking
    progress = st.progress(0)
    status = st.empty()
    
    # Run the research process
    from main import main
    
    try:
        # Show spinner during execution
        with st.spinner(f"Researching {company_name}..."):
            # Step 1: Industry Research (25%)
            status.text("Step 1/4: Conducting industry research...")
            progress.progress(10)
            
            # Import necessary modules
            from agents.industry_research_agent import create_industry_research_agent
            
            # Run industry research
            industry_research_agent, industry_research_prompt = create_industry_research_agent()
            industry_research_query = industry_research_prompt.format(industry_or_company=company_name)
            industry_research_output = industry_research_agent.invoke(industry_research_query)
            industry_research_text = (
                industry_research_output.get("output", "") 
                if isinstance(industry_research_output, dict) else industry_research_output
            )
            progress.progress(25)
            
            # Step 2: Use Case Generation (50%)
            status.text("Step 2/4: Generating AI use cases...")
            from agents.use_case_agent import create_use_case_agent
            use_case_agent, _ = create_use_case_agent()
            use_case_output = use_case_agent.invoke({"industry_research": industry_research_text})
            use_cases_text = use_case_output.content
            progress.progress(50)
            
            # Step 3: Resource Collection (75%)
            status.text("Step 3/4: Finding relevant resources...")
            from agents.resource_agent import create_resource_agent
            resource_agent, resource_prompt = create_resource_agent()
            resource_query = resource_prompt.format(use_cases=use_cases_text)
            resource_output = resource_agent.invoke(resource_query)
            resource_text = (
                resource_output.get("output", "") 
                if isinstance(resource_output, dict) else resource_output
            )
            progress.progress(75)
            
            # Step 4: Final Proposal Generation (100%)
            status.text("Step 4/4: Creating final proposal...")
            from agents.final_proposal_agent import create_final_proposal_agent
            final_proposal_agent, _ = create_final_proposal_agent()
            final_proposal_output = final_proposal_agent.invoke({
                "industry_research": industry_research_text,
                "use_cases": use_cases_text,
                "resource_links": resource_text,
                "company_name": company_name
            })
            final_proposal_text = final_proposal_output.content
            progress.progress(100)
            
        # Save results to files
        with open(os.path.join("output", "industry_research.md"), "w") as f:
            f.write(industry_research_text)
        with open(os.path.join("output", "use_cases.md"), "w") as f:
            f.write(use_cases_text)
        with open(os.path.join("output", "resource_links.md"), "w") as f:
            f.write(resource_text)
        with open(os.path.join("output", "final_proposal.md"), "w") as f:
            f.write(final_proposal_text)
        
        # Display results in tabs
        status.empty()
        st.success(f"Research completed for {company_name}!")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "Industry Research", 
            "Use Cases", 
            "Resources", 
            "Final Proposal"
        ])
        
        with tab1:
            st.markdown(industry_research_text)
            st.download_button(
                "Download Industry Research", 
                industry_research_text,
                f"{company_name.replace(' ', '_')}_industry_research.md"
            )
            
            # Generate word cloud from industry research
            from wordcloud import WordCloud
            import matplotlib.pyplot as plt
            
            st.subheader("Key Terms Analysis")
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(industry_research_text)
            
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
            
        with tab2:
            st.markdown(use_cases_text)
            st.download_button(
                "Download Use Cases", 
                use_cases_text,
                f"{company_name.replace(' ', '_')}_use_cases.md"
            )
            
        with tab3:
            st.markdown(resource_text)
            st.download_button(
                "Download Resource Links", 
                resource_text,
                f"{company_name.replace(' ', '_')}_resources.md"
            )
            
        with tab4:
            st.markdown(final_proposal_text)
            st.download_button(
                "Download Final Proposal", 
                final_proposal_text,
                f"{company_name.replace(' ', '_')}_proposal.md"
            )
        
        # Add below tabs
        st.subheader("Export Options")
        export_format = st.radio("Export Format:", ["Markdown", "PDF", "Word", "Presentation"])
        if st.button("Export All"):
            # Logic for exporting in selected format
            st.success(f"Exported as {export_format}")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your API keys and try again.")