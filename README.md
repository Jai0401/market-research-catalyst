# AI-Powered Market Research and Proposal Generation
This project automates the process of market research, use case generation, resource discovery, and final proposal creation using a multi-agent system powered by Large Language Models (LLMs) and Generative AI (GenAI). It leverages the Gemini API and a web browser tool to gather information, generate ideas, and create a comprehensive proposal document.

![workflow](workflow.svg)

## Getting Started
### Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Jai0401/market-research-catalyst.git
    cd market-research-catalyst
    ```
    
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```
    
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    
### Configuration
1.  **Set up environment variables:**
    *   Create a `.env` file in the project root directory.
    *   Add your Gemini API key and Exa API key to the `.env` file:
        ```
        GEMINI_API_KEY=<your_gemini_api_key>
        EXA_API_KEY=<your_exa_api_key>
        ```
        
2.  **Configure the industry to research:**
    *   Open the `config.py` file.
    *   Modify the `COMPANY_OR_INDUSTRY_TO_RESEARCH` variable to the desired industry or company:
        ```python
        COMPANY_OR_INDUSTRY_TO_RESEARCH = "Agriculture"  # Example: "Healthcare"
        ```
        
## Usage
### Running the Pipeline
1.  **Run the `main.py` script:**
    ```bash
    python3 main.py
    ```
    This will execute the multi-agent system, performing market research, generating use cases, collecting resources, and creating the final proposal. The outputs will be saved in the `output` directory.



## [Project Report](https://github.com/Jai0401/market-research-catalyst/blob/main/project-report.md)
