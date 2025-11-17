from core.agent_session import AgentSession
from core.memory_bank import MemoryBank
from core.agent_orchestrator import AgentOrchestrator

import argparse

def run_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="CSV file to analyze")
    args = parser.parse_args()

    session = AgentSession()
    memory = MemoryBank()
    orchestrator = AgentOrchestrator(session, memory)

    report = orchestrator.run(args.file)

    print("\n=========== FINAL REPORT ===========\n")
    print(report)

if __name__ == "__main__":
    run_cli()
