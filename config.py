import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EXA_API_KEY = os.getenv("EXA_API_KEY")

COMPANY_OR_INDUSTRY_TO_RESEARCH = "Scale AI" # Change this to the industry or company you want to research in UI 
# Change the name of comapny here when running locally by running the 'main.py' file