# FinBuddy — Multi-Agent Personal Finance Analyzer

### 🎯 Problem  
People struggle to understand their spending habits and make informed financial decisions. Raw transaction data (CSV) is messy and unclear.

### 💡 Solution  
FinBuddy is a modular, multi-agent, LLM-powered financial analysis system designed to transform raw banking transaction CSV files into categorized data, behavioral insights, personalized recommendations, and a structured financial report.

### 🧠 Why Agents?  
Each task requires reasoning autonomy:
- Categorization requires classification.
- Insights require pattern analysis.
- Recommendations require financial reasoning.
- Reporting requires structured language generation.

Agents also allow modularity, scalability, and easy debugging.

## Architecture
FinBuddy uses a clean, extensible multi-agent architecture:

### **Agents**
- **CategorizerAgent** – Classifies each transaction into spending categories.
- **InsightsAgent** – Detects patterns, anomalies, monthly trends, and spending behaviors.
- **RecommenderAgent** – Generates personalized financial advice.
- **ReporterAgent** – Produces the final structured financial summary & report.

### **System Components**
- **Orchestrator** – Controls the pipeline flow between agents.
- **CSV Tool** – Ingests, validates, cleans, and preprocesses CSV files.
- **Session Manager** – Tracks state within a single run.
- **MemoryBank** – Cross-run persistent memory for long-term learning.
- **Hybrid LLM Client** – Routes prompts to OpenAI or LM Studio based on availability.

## Hybrid LLM Execution
FinBuddy includes a **HybridClient** that automatically chooses the LLM backend:

### Priority Order
1. **OpenAI (cloud)**  
2. **LM Studio local API**  
   - Example endpoint:  
     `http://192.168.50.230:1234/v1`
   - Example model:  
     `"gpt2-smashed"`

### LM Studio Python Integration
FinBuddy uses the OpenAI Python client to communicate with LM Studio:

```python
import openai

openai.api_base = "http://192.168.50.230:1234/v1"
openai.api_key = "not-needed"

response = openai.ChatCompletion.create(
    model="gpt2-smashed",
    messages=[{"role": "user", "content": "Hello from FinBuddy"}]
)

print(response.choices[0].message.content)
```

### 🏛 Architecture

                    ┌───────────────────────────┐
                    │      User's CSV File      │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                         ┌────────────────┐
                         │   CSV Tool     │
                         │ (tools/csv...) │
                         └───────┬────────┘
                                 │  Raw DataFrame
                                 ▼
                     ┌───────────────────────────┐
                     │    Categorizer Agent      │
                     │ agents/categorizer_agent  │
                     └─────────────┬─────────────┘
                                   │ Categorized DF
                                   ▼
                     ┌───────────────────────────┐
                     │      Insights Agent       │
                     │ agents/insights_agent     │
                     │  + MemoryBank (core/)     │
                     └─────────────┬─────────────┘
                                   │ Insights
                                   ▼
                     ┌───────────────────────────┐
                     │   Recommender Agent       │
                     │ agents/recommender_agent  │
                     └─────────────┬─────────────┘
                                   │ Recommendations
                                   ▼
                     ┌───────────────────────────┐
                     │      Reporter Agent       │
                     │ agents/reporter_agent     │
                     └─────────────┬─────────────┘
                                   │ Final Report
                                   ▼
                           ┌─────────────────┐
                           │    CLI Output    │
                           │    (main.py)     │
                           └─────────────────┘

       ┌────────────────────────────────────────────────────────────┐
       │           Session (core/agent_session.py)                  │
       └────────────────────────────────────────────────────────────┘

       ┌────────────────────────────────────────────────────────────┐
       │           MemoryBank (core/memory_bank.py)                 │
       └────────────────────────────────────────────────────────────┘

### File Structure

finbuddy/
│
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

###📦 Installation
