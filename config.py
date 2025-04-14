# Purpose: Centralized environment and API key management

import os
from dotenv import load_dotenv

# Load .env file into environment
load_dotenv()

# Export constants for use throughout the project
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
