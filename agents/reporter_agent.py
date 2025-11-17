#from core.openai_client import client
from core.hybrid_client import generate
from tqdm import tqdm

class ReporterAgent:
    def run(self, df, insights, recs):
        print("[ReporterAgent] Starting report generation...")
        prompt = f"""
Create a structured financial report including:

1. Summary of transaction categories
2. Monthly insights
3. Personalized recommendations

Data sample:
{df.head()}

Insights:
{insights}

Recommendations:
{recs}
"""
        for _ in tqdm(range(1), desc="Generating Report"):
            report = generate(prompt, max_tokens=300)

        print("[ReporterAgent] Report generation completed.")
        return report.strip()
