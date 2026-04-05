import re 
import requests
import os
from dotenv import load_dotenv
load_dotenv()
class HiringAgent:
    def __init__(self,github_token=None):
        self.ai_patterns = [
            "rapidly evolving landscape", "I'd be happy to assist", "comprehensive overview", "leveraging my expertise" ,"it's important to note", "as an ai model"
        ]
        self.tech_keywords = {'python','playwright','fastapi','redis','docker','async','scraping','agent'}
        self.action_keywords = {'implemented','optimized','solved','debugged','built','fixed'}
        self.headers = {"Authorization": f"token {github_token}"} if github_token else {} # to avoid github rate limit 
    
    def clean_input(self,data):
        return {
            "name": str(data.get("name","Unknown")),
            "github": str(data.get("github","")).lower(),
            "answer": str(data.get("answer",""))
        }
    
    def get_github_signal(self, github_url):
        if 'github.com' not in github_url:
            return -30 , "github not provided"
        try:
            username = github_url.split('/')[-1]
            api_url = f"https://api.github.com/users/{username}/repos"
            response = requests.get(api_url, headers = self.headers, timeout=5)

            if response.status_code == 403:
                return 0,"github limit exhausted"
            if response.status_code != 200:
                return -10 ,"github profile invalid"

            repos = response.json()
            if not repos:
                return -20,"empty github profile"
            original_repos = [r for r in repos if not r['fork']]
            stars = sum(r['stargazers_count'] for r in repos)

            if len(original_repos) > 5 and stars > 2:
                return 40,"active builder"
            elif len(original_repos) > 0:
                return 25,f"standard: {original_repos} original repos"
            else:
                return -10,"Low quality"
        except Exception as e:
            return 0, f"error checking github: {str(e)}"

    
    def get_answer_quality_depth_signal(self, answer):

        if(len(answer)< 20):
            return -30,"Low effort answer"
        
        score = 0
        words = set(re.findall(r'\w+', answer.lower()))

        tech_hits = words.intersection(self.tech_keywords)
        score += (len(tech_hits)*15)

        action_hits = words.intersection(self.action_keywords)
        score += (len(action_hits) * 15)

        return score,f"Signals: {list(tech_hits)} | {list(action_hits)}"
    
    def detect_ai_penalty(self,answer):
        penalty = 0
        for pattern in self.ai_patterns:
            if pattern in answer.lower():
                penalty -= 30
        return penalty
    

    def evaluate_candidate(self,raw_data):

        candidate = self.clean_input(raw_data)

        final_score = 50
        report_logs = []

        git_score,git_msg = self.get_github_signal(candidate["github"])
        final_score += git_score
        report_logs.append(git_msg)

        answer_quality_score, answer_quality_msg = self.get_answer_quality_depth_signal(candidate["answer"])
        final_score += answer_quality_score
        report_logs.append(answer_quality_msg)

        ai_penality = self.detect_ai_penalty(candidate["answer"])
        final_score += ai_penality
        if ai_penality < 0: 
            report_logs.append("AI pattern detected")
        
        tier = "REJECT"
        if final_score > 110: 
            tier = "fast-track"
        elif final_score > 60:
            tier = "standard"
        
        return {
            "name": candidate["name"],
            "score": final_score,
            "tier": tier,
            "report": "|".join(report_logs)
        }
    

    

if __name__ == "__main__":
    my_token = os.getenv("GITHUB_TOKEN")
    agent = HiringAgent(github_token=my_token) 
    
    # Test with 3 types of candidates
    test_data = [
        {"name": "Real Dev", "github": "https://github.com/realuser/project", "answer": "I built a scraper using Playwright and solved rate limits."},
        {"name": "AI Bot", "github": "https://github.com/bot", "answer": "In the rapidly evolving landscape of AI, I leverage my expertise..."},
        {"name": "Empty", "github": "", "answer": ""}
    ]

    for data in test_data:
        result = agent.evaluate_candidate(data)
        print(f"Candidate: {result['name']} | Score: {result['score']} | Tier: {result['tier']}")
        


   