
# Autonomous Hiring Agent Prototype - GenoTek Challenge

A modular, state-driven AI agent designed to automate end-to-end recruitment on platforms like Internshala.

## 🚀 Core Architecture
This system is built as a **State-Machine**. Unlike simple linear scripts, it maintains candidate context across multiple rounds of interaction.

- **Scoring Engine (`agent_prototype.py`):** Uses a heuristic weighting system to evaluate Technical Density (Tech Stack + Action Verbs) and GitHub quality (Fork-Ratio analysis).
- **Engagement Manager (`engagement_manager.py`):** A stateful IMAP/SMTP handler that tracks conversation history and manages email threading via `References` headers.
- **Anti-Cheat Logic (`anticheat.py`):** Implements semantic similarity analysis to detect LLM-generated templates.
- **Self-Learning Loop:** Analyzes "Fast-Tracked" candidates to update high-signal keyword weights dynamically.

## 🛠️ Key Findings & Lessons Learned
During development and live-testing, I identified several "Production-level" hurdles:

1. **State Poisoning:** In early tests, the IMAP fetch was too broad, causing the agent to "recruit" system notifications (Google/Instagram). I solved this by implementing a **Targeted Polling** mechanism that only processes whitelisted candidate addresses.
2. **Access Obstacles:** Identified **reCAPTCHA Enterprise (Invisible)** on the Internshala login. Proposed a **Session-Injection** strategy to maintain persistent headless access.
3. **GitHub Signal Noise:** Discovered that 80%+ of applicants are "Tutorial Collectors." Developed a **Fork-Ratio** algorithm to verify original code authorship.
4. **Email Threading:** Identified that `In-Reply-To` headers are insufficient for modern Gmail threading; implemented full `References` chain persistence.

## 📦 Setup & Run
1. Install requirements: `pip install requests sentence-transformers`
2. Configure credentials in `engagement_manager.py`.
3. Run the evaluation: `python agent_prototype.py`
4. Run the email test: `python test_engagement.py`