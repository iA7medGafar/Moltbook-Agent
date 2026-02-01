# 🦞 Moltbook Autonomous Agent (Secure Sniper)

An autonomous AI agent designed to interact with the **Moltbook** social network protocol. This bot monitors the network in real-time for financial opportunities (MBC-20 tokens) and automates interactions securely using a clean REST API implementation.

## 🚀 Key Features

- **🛡️ Secure Architecture:** API keys are isolated in a local `config.py` file and are **never exposed** to version control (verified via `.gitignore`).
- **⚡ High Performance:** Uses `requests` library for direct API communication (no heavy browser/Selenium required).
- **🤖 Pattern Recognition:** Automatically detects `{"op": "mint"}` JSON patterns using Regex to identify valid minting opportunities.
- **⏱️ Smart Rate Limiting:** Respects Moltbook's API limits (429 handling) to prevent bans.
- **💰 Auto-Sniper:** Automatically replies to minting posts within seconds to secure tokens.

## 🛠️ Tech Stack

- **Python 3.x**
- **Requests** (HTTP Client)
- **Regular Expressions (Regex)**
- **Git** (Version Control)

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/iA7medGafar/Moltbook-Agent.git](https://github.com/iA7medGafar/Moltbook-Agent.git)
   cd Moltbook-Agent
