#from core.openai_client import client
from core.hybrid_client import generate
from tqdm import tqdm

class InsightsAgent:
    def run(self, df, memory):
        print("[InsightsAgent] Starting insight generation...")
        monthly_total = df["Amount"].sum()
        frequent = df["Description"].value_counts().idxmax()
        history = memory.get_history() if memory else "No history"

        prompt = f"""
Analyze the following:
- This month's total spending: {monthly_total}
- Most frequent merchant: {frequent}
- Past behaviors: {history}

Produce 5 insights.
"""
        for _ in tqdm(range(1), desc="Generating Insights"):
            insights = generate(prompt, max_tokens=200)

        print(f"[InsightsAgent] Insights received:\n{insights.strip()}")
        return insights.strip()
