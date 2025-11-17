# FinBuddy – Multi‑Agent Financial Intelligence System

[![GitHub license](https://img.shields.io/github/license/your-username/finbuddy_agents.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT4.1-orange.svg)](https://openai.com)
[![LM Studio](https://img.shields.io/badge/LM_Studio-local-green.svg)](https://lmstudio.ai)

---

## 📌 Overview

FinBuddy is a modular, LLM‑powered pipeline that turns raw banking transactions into:

| Output | Description |
|--------|-------------|
| **Cleaned & categorized data** | Standardised transaction descriptions and categories |
| **Spending pattern insights** | Anomalies, trends, and key metrics |
| **Personalised recommendations** | Actionable advice tailored to the user |
| **Structured financial report** | Summary ready for presentation or further analysis |

The system is built for reliability: it automatically falls back from OpenAI to a local LM Studio model when quotas are exhausted, while keeping execution offline‑friendly.

---

## 🚀 Features

- **Multi‑Agent Architecture** – Four specialised agents work in lockstep:
  1. `CategorizerAgent` – Cleans and classifies transaction descriptions  
  2. `InsightsAgent` – Detects anomalies & spending trends  
  3. `RecommenderAgent` – Generates personalised financial advice  
  4. `ReporterAgent` – Produces the final structured report
- **Hybrid Cloud + Local LLM Execution** – Automatic fallback from OpenAI to LM Studio (`gpt2-smashed`) when quotas fail.
- **Observability** – Console logs, per‑agent progress bars, and detailed tracebacks.  
  Fail‑fast logic stops after two consecutive failures to avoid noisy results.
- **Session & Memory Management** – Session logs for each run and a `MemoryBank` that compares behaviour across sessions.

---

## 🏗️ System Architecture

                    ┌───────────────────────────┐
                    │      User's CSV File      │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                         ┌────────────────┐
                         │    CSV Tool    │
                         └───────┬────────┘
                                 │ Raw DataFrame
                                 ▼
                     ┌────────────────────────────┐
                     │      Categorizer Agent     │
                     └─────────────┬──────────────┘
                                   │ Categorized DF
                                   ▼
                     ┌────────────────────────────┐
                     │       Insights Agent       │
                     │     + MemoryBank           │
                     └─────────────┬──────────────┘
                                   │ Insights
                                   ▼
                     ┌────────────────────────────┐
                     │     Recommender Agent      │
                     └─────────────┬──────────────┘
                                   │ Recommendations
                                   ▼
                     ┌────────────────────────────┐
                     │       Reporter Agent        │
                     └─────────────┬──────────────┘
                                   │ Final Report
                                   ▼
                           ┌─────────────────┐
                           │    CLI Output    │
                           └─────────────────┘

| Component     | Technology                                        |
| ------------- | ------------------------------------------------- |
| LLMs          | OpenAI GPT-4.1 / GPT-4.1-mini / LM Studio (local) |
| Language      | Python 3.10+                                      |
| Libraries     | pandas, tqdm, python-dotenv, requests, openai     |
| Architecture  | Multi-agent orchestrated pipeline                 |
| Observability | Logging, progress bars, verbose tracing           |

## 📦 Installation

```python
git clone <your-repo-url>
cd finbuddy_agents
pip install -r requirements.txt
```
Create a .env file:
```
OPENAI_API_KEY=your_api_key
```
⚠️ Must be named exactly .env

## ▶️ Usage
Run the pipeline:
```
python main.py data/sample_transactions.csv
```
You will see:
✔ Progress bars per agent
✔ Detailed logs of LLM calls
✔ Hybrid model fallback messages
✔ Final financial report

## 📁 Project Structure
    finbuddy/│
    ├── agents/
    │   ├── categorizer.py
    │   ├── insights.py
    │   ├── recommender.py
    │   └── reporter.py
    │
    ├── tools/
    │   ├── csv_tool.py
    │   └── memory.py
    │
    ├── core/
    │   ├── orchestrator.py
    │   ├── hybrid_client.py
    │   └── session_manager.py
    │
    ├── data/
    ├── main.py
    └── README.md



## 🧩 Hybrid LLM Execution Logic

The hybrid client works as follows:
1. Try OpenAI cloud
2. If "insufficient_quota" or other failure →
   ➜ automatically retry using LM Studio
3. If LM Studio responds with "Returning 200 anyway" →
   ➜ hard stop (protects from invalid results)
4. Stop after 2 total failures

## 🛠️ Extending FinBuddy
Adding a new agent
Create file under /agents
Implement:
```
def run(self, df, session):
....
```
Register agent in agent_orchestrator.py

Adding new tools
1. Add under /tools
2. Follow clean modular import structure

## 🪵 Logging & Debugging
FinBuddy logs:
   * API provider used (OpenAI or LM Studio)
   * Raw LM Studio responses
   * Retry counts
   * Agent-level timings
   * DataFrame previews
   * Full progress bars
This makes it deeply transparent and ideal for debugging or Kaggle demonstrations.

## 📝 License
MIT License
You’re free to modify and use for personal or commercial use.
