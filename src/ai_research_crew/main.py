#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from ai_research_crew.crew import AiResearchCrew
from ai_research_crew.render import render_markdown
from ai_research_crew.models import VerifiedReport
from pydantic import BaseModel

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': str(input("Please Provide the Topic to research").strip()),
        'current_year': str(datetime.now().year)
    }

    try:
        result = AiResearchCrew().crew().kickoff(inputs=inputs)
        # the last task's structured output
        verified_report: VerifiedReport = result.pydantic
        markdown = render_markdown(verified_report, inputs['topic'])

        os.makedirs("output", exist_ok=True)
        with open("output/research_report.md", "w", encoding="utf-8") as f:
            f.write(markdown)

        print("Report written to output/research_report.md")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        AiResearchCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AiResearchCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        AiResearchCrew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = AiResearchCrew().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
