import pandas as pd
import time
from agents.categorizer_agent import CategorizerAgent
from agents.insights_agent import InsightsAgent
from agents.recommender_agent import RecommenderAgent
from agents.reporter_agent import ReporterAgent
from tools.csv_tool import CSVTool
from tqdm import tqdm

class AgentOrchestrator:
    """
    Orchestrates all agents with:
    - Overall pipeline progress bar
    - Detailed per-agent progress bars
    - Retry mechanism: stops after 2 consecutive failed runs
    """

    def __init__(self, session, memory, max_retries=2):
        self.session = session
        self.memory = memory
        self.max_retries = max_retries
        self.categorizer = CategorizerAgent()
        self.insights = InsightsAgent()
        self.recommender = RecommenderAgent()
        self.reporter = ReporterAgent()

    def _run_with_retry(self, func, *args, stage_name="Stage"):
        """
        Runs a function with retry. Stops after max_retries if consecutive failures occur.
        """
        retries = 0
        while retries < self.max_retries:
            try:
                print(f"[Orchestrator] Running {stage_name}, attempt {retries + 1}")
                result = func(*args)
                print(f"[Orchestrator] {stage_name} completed successfully.")
                return result
            except Exception as e:
                retries += 1
                print(f"[Orchestrator] {stage_name} failed: {e}")
                if retries < self.max_retries:
                    print(f"[Orchestrator] Retrying {stage_name} (attempt {retries + 1})...")
                    time.sleep(1)  # small delay before retry
                else:
                    print(f"[Orchestrator] {stage_name} failed {self.max_retries} times. Stopping pipeline.")
                    raise e  # stop the pipeline

    def run(self, file_path):
        stages = ["Categorizing", "Insights", "Recommendations", "Report"]

        print("[Orchestrator] Loading CSV file:", file_path)
        raw_df = pd.read_csv(file_path)
        print("[Orchestrator] CSV loaded. Sample:")
        print(raw_df.head())

        results = {}
        for stage in tqdm(stages, desc="Pipeline Progress", ncols=100):
            if stage == "Categorizing":
                results["categorized"] = self._run_with_retry(
                    self.categorizer.run, raw_df, self.session, stage_name="Categorizing"
                )

            elif stage == "Insights":
                results["insights"] = self._run_with_retry(
                    self.insights.run, results["categorized"], self.memory, stage_name="Insights"
                )

            elif stage == "Recommendations":
                results["recommendations"] = self._run_with_retry(
                    self.recommender.run, results["insights"], stage_name="Recommendations"
                )

            elif stage == "Report":
                results["report"] = self._run_with_retry(
                    self.reporter.run,
                    results["categorized"],
                    results["insights"],
                    results["recommendations"],
                    stage_name="Report"
                )

        print("\n[Orchestrator] All agents completed successfully.")
        return results["report"]