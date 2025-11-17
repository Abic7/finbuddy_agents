# FinBuddy — Multi-Agent Personal Finance Analyzer

### 🎯 Problem  
People struggle to understand their spending habits and make informed financial decisions. Raw transaction data (CSV) is messy and unclear.

### 💡 Solution  
FinBuddy uses a **multi-agent LLM system** to automatically categorize spending, derive insights, store long-term behaviors, and generate personalized financial recommendations.

### 🧠 Why Agents?  
Each task requires reasoning autonomy:
- Categorization requires classification.
- Insights require pattern analysis.
- Recommendations require financial reasoning.
- Reporting requires structured language generation.

Agents also allow modularity, scalability, and easy debugging.

---

# 🏛 Architecture

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
