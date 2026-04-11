from agent_prototype import HiringAgent
from engagement_manager import EngagementManager
import time
import os
from dotenv import load_dotenv
import pandas as pd
import database as db
import sqlite3
load_dotenv()

class Recruit:
    def __init__(self):
        db.init_db()
        self.scorer = HiringAgent()
        self.mailer = EngagementManager(os.getenv("EMAIL"),os.getenv("APP_PASSWORD"))
    
    def ingest_csv(self,filepath):

        if not os.path.exists(filepath):
            print(f"Error: {filepath} not found.")
            return
        
        df = pd.read_csv(filepath)
        for index,row in df.iterrows():
            raw_data = {
                "name": row.get('Name'),
                "github": row.get('Github URL'),
                "answer": row.get('Answer'),
                "email": row.get('Email')
            }
            result = self.scorer.evaluate_candidate(raw_data)

            if result['tier'] != "REJECT":
                db.save_scored_candidate(raw_data['email'], raw_data['name'],result['score'],result['tier'])
                print(f"Added {raw_data['name']} to to database (Score: {result['score']})")

    def process_outreach(self):
        """Finds scored candidates who haven't been emailed yet and contacts them."""
        connection = sqlite3.connect('recruit.db')
        c = connection.cursor()
        c.execute("SELECT email, name, score FROM candidates WHERE status = 'SCORED'")
        
        for email, name, score in c.fetchall():
            print(f"Sending initial outreach to {name}...")
            msg_id = self.mailer.send_threaded_mail(
                email, 
                "Interview Round 1", 
                f"Hi {name}, your technical score was {score}. Can you tell us more about your experience?"
            )
            
            db.update_mail_state(email, msg_id, "", 1)
        connection.close()
        
    def run_polling_loop(self):
        while True:
            print("checking for candidate replies")
            self.mailer.read_replies()
            time.sleep(300)

    

if __name__ == "__main__":
    system = Recruit()


                
