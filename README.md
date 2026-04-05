
# Autonomous Hiring Agent - GenoTek Submission

## 📦 Installation & Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install requests python-dotenv sentence-transformers
   ```
3. Create a `.env` file in the root directory (refer to `.env.example`).
4. Enable **IMAP** in your Gmail settings and generate an **App Password**.

## 🚀 Running the Modules

### 1. Scoring & Intelligence Engine
To test the candidate ranking, GitHub analysis, and anti-cheat logic:
```bash
python agent_prototype.py
```

### 2. Engagement & Threading Test
To run a live simulation of the multi-round threaded email system:
1. Run the test script: `python test_engagement.py`
2. Follow the terminal prompts to reply to the automated outreach.
3. Observe the agent identifying your technical keywords and sending a threaded follow-up.

### 3. Anti-Cheat Semantic Check
To verify the LLM-similarity detection:
```bash
python anticheat.py
```

## 🧠 Technical Highlights
- **Stateful Threading:** Uses `References` headers to maintain 100% thread continuity in Gmail.
- **Heuristic Scoring:** Weights **Technical Density** (Action Verbs + Tech Stack) against **GitHub Fork-Ratio**.
- **Conflict Handling:** Specifically designed to ignore "System Noise" (Google/Instagram notifications) using a **Targeted Whitelist Polling** strategy.