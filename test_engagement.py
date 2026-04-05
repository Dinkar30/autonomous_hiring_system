from engagement_manager import EngagementManager
import time
import os
from dotenv import load_dotenv
load_dotenv()
RECRUITER_EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
CANDIDATE_EMAIL = "dinkar.gdsc.ai@gmail.com"


if os.path.exists("candidate_states.json"):
    os.remove("candidate_states.json")
manager = EngagementManager(RECRUITER_EMAIL, APP_PASSWORD)

def run_test():
    print(f"--- STEP 1: CONTACTING REAL CANDIDATE: {CANDIDATE_EMAIL} ---")
    first_msg_id = manager.send_threaded_mail(
        recipient=CANDIDATE_EMAIL,
        subject="AI Agent Developer Internship - Round 1",
        body="Hi! Thanks for applying. Can you tell me which technologies you used in your latest project?"
    )
    print(f"Initial Message ID: {first_msg_id}")


    print("\n--- STEP 2: HUMAN ACTION REQUIRED ---")
    print(f"1. Log in to {CANDIDATE_EMAIL}")
    print("2. Look for the 'Round 1' email.")
    print("3. Reply with: 'I used Redis and FastAPI for my backend.'")
    print("4. Wait 10 seconds, then come back here and press Enter.")
    input("Press Enter once you have replied to the email...")


    print("\n--- STEP 3: AGENT READING REPLIES ---")
    # This should find the UNSEEN reply, analyze it, and send a THREADED follow-up
    manager.read_replies()
    
    print("\n--- STEP 4: VERIFICATION ---")
    print(f"Check {CANDIDATE_EMAIL} again.")
    print("You should see a NEW reply in the SAME thread asking about Redis/FastAPI.")

if __name__ == "__main__":
    run_test()
