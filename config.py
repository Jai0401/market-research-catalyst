import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EXA_API_KEY = os.getenv("EXA_API_KEY")

COMPANY_OR_INDUSTRY_TO_RESEARCH = "Healthcare" # Change this to the industry or company you want to research