import pandas as pd
#from core.openai_client import client
from core.hybrid_client import generate
from tqdm import tqdm

class CategorizerAgent:
    """
    Categorizes transactions using the hybrid LLM client.
    """

    def run(self, df, session):
        print("[CategorizerAgent] Starting categorization of transactions...")
        cleaned = []

        for i, row in enumerate(tqdm(df.itertuples(), total=len(df), desc="Categorizing")):
            description = row.Description
            category = generate(
                prompt=f"Categorize this transaction into a financial category: {description}",
                max_tokens=50
            )
            cleaned.append(category.strip())

        df["Category"] = cleaned
        session.log("CategorizerAgent completed")
        print("[CategorizerAgent] Completed categorization.")
        return df