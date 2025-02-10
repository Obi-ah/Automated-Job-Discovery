from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Default Scraper Settings
BASE_URL = os.getenv("BASE_URL")
JOB_TITLE = os.getenv("JOB_TITLE")
JOB_LOCATION = os.getenv("JOB_LOCATION")
JOB_DAYS_SINCE_POSTED = int(os.getenv("JOB_DAYS_SINCE_POSTED"))
MAX_PAGES = int(os.getenv("MAX_PAGES"))

USER_AGENTS = [
    os.getenv("USER_AGENT_1"),
    os.getenv("USER_AGENT_2"),
    os.getenv("USER_AGENT_3")
]

# Filter out None values if any USER_AGENT_* is missing
USER_AGENTS = [ua for ua in USER_AGENTS if ua]

# Output Configuration
OUTPUT_FILE = os.getenv("OUTPUT_FILE")

# Debug
if __name__ == "__main__":
    print(f"BASE_URL: {BASE_URL}")
    print(f"JOB_TITLE: {JOB_TITLE}")
    print(f"JOB_LOCATION: {JOB_LOCATION}")
    print(f"JOB_DAYS_SINCE_POSTED: {JOB_DAYS_SINCE_POSTED}")
    print(f"MAX_PAGES: {MAX_PAGES}")
    print(f"USER_AGENTS: {USER_AGENTS}")
    print(f"OUTPUT_FILE: {OUTPUT_FILE}")