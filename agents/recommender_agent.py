#from core.openai_client import client

from core.hybrid_client import generate
from tqdm import tqdm

class RecommenderAgent:
    def run(self, insights):
        print("[RecommenderAgent] Starting recommendation generation...")
        prompt = f"Based on these insights, generate 5 actionable financial recommendations:\n{insights}"

        for _ in tqdm(range(1), desc="Generating Recommendations"):
            recs = generate(prompt, max_tokens=150)

        print(f"[RecommenderAgent] Recommendations received:\n{recs.strip()}")
        return recs.strip()
