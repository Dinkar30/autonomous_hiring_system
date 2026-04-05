import smtplib
from email.mime.text import MIMEText
from email.utils import make_msgid, parseaddr
import imaplib, email
import json,os

class EngagementManager:
    def __init__(self, smtp_user, smtp_password):
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.candidate_states = {}
        self._load_state()

    def _save_state(self):
        with open("candidate_states.json", "w") as f:
            json.dump(self.candidate_states, f) 

    def _load_state(self):
        if os.path.exists("candidate_states.json"):
            with open("candidate_states.json") as f:
                self.candidate_states = json.load(f)

    def analyze_reply(self,reply_text):
        text = reply_text.lower()
        tech_keywords = ['redis', 'docker' ,'fastapi', 'async', 'playwright']
        hits = [tech for tech in tech_keywords if tech in text]
        if hits:
            return "Technical depth",f"You mentioned {','.join(hits)} , can you walk us through how you used them together ?"
        
        return "STANDARD_FOLLOW_UP", "We've got your details , what was the most challenging task or problem you solved in this project ?"
    
    def send_threaded_mail(self, recipient , subject,body , prev_message_id =None):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['To'] = recipient
        msg['From'] = 'recruiter@genotek.global'

        # for threading
        new_msg_id = make_msgid()
        msg['Message-id'] = new_msg_id

        if prev_message_id:
            msg['In-Reply-To'] = prev_message_id
            prev_refs = self.candidate_states.get(recipient, {}).get("references", "")
            msg['References'] = f"{prev_refs} {prev_message_id}".strip()
            self.candidate_states[recipient]["references"] = msg['References']
            print(f"Threaded reply sent to {recipient}")
        else:
            print(f"New thread started with {recipient}")
        print(f"Content: {body}\n")
        
        #updating and persisting states
        state = self.candidate_states.get(recipient, {"references": "" , "round": 0})
        state.update({
        "last_msg_id": new_msg_id,
        "round": state.get("round", 0) + 1,
        "references": msg.get('References',"")
        })
        self.candidate_states[recipient] = state
        self._save_state()

        with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
            server.login(self.smtp_user,self.smtp_password)
            server.sendmail(self.smtp_user,recipient, msg.as_string())

        return new_msg_id
    
    def get_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        return msg.get_payload(decode=True).decode()
    

    
    def read_replies(self):
        with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
            mail.login(self.smtp_user,self.smtp_password)
            mail.select("inbox")
         
            for candidate_email in self.candidate_states.keys():
                search_query = f'(UNSEEN FROM "{candidate_email}")'
                _, data = mail.search(None, search_query)
                for num in data[0].split():
                    _, msg_data = mail.fetch(num, '(RFC822)')
                    msg = email.message_from_bytes(msg_data[0][1])
                    body = self.get_body(msg)
                    _, follow_up = self.analyze_reply(body)
                
                    # need prev message id for threading
                    prev_id = self.candidate_states.get(candidate_email, {}).get("last_msg_id")
                    self.send_threaded_mail(candidate_email, "Re: Your Application", follow_up, prev_id)       

                    mail.store(num, '+FLAGS', '\\Seen')
                    print(f"SUCCESS: Replied to candidate {candidate_email}")                     


