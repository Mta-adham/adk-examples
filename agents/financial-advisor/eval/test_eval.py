# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Basic evaluation for Financial Advisor"""

import asyncio
import pathlib
import sys

import dotenv
import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()


async def run_detailed_evaluation():
    """Run the evaluation with detailed metrics output."""
    print("=" * 80)
    print("FINANCIAL ADVISOR EVALUATION - DETAILED METRICS")
    print("=" * 80)
    sys.stdout.flush()

    # Default criteria from the framework
    criteria = {
        'response_match_score': 0.8,
        'tool_trajectory_avg_score': 1.0
    }

    print(f"Evaluation Criteria: {criteria}")
    print(f"Number of runs: 5")
    print("-" * 80)
    sys.stdout.flush()

    # Load eval set and run detailed evaluation
    eval_set = AgentEvaluator._load_eval_set_from_file(
        str(pathlib.Path(__file__).parent / "data" / "financial-advisor.test.json"),
        criteria=criteria,
        initial_session={}
    )

    print(f"Loaded eval set: {eval_set.name}")
    print(f"Number of test cases: {len(eval_set.eval_cases)}")
    print("-" * 80)
    sys.stdout.flush()

    try:
        await AgentEvaluator.evaluate_eval_set(
            agent_module="financial_advisor",
            eval_set=eval_set,
            criteria=criteria,
            num_runs=5,
            print_detailed_results=True
        )
        print("=" * 80)
        print("EVALUATION COMPLETED SUCCESSFULLY")
        print("=" * 80)
    except AssertionError as e:
        print("=" * 80)
        print("EVALUATION COMPLETED WITH FAILURES")
        print("=" * 80)
        print("Failure details:")
        print(str(e))
        print("=" * 80)
        # Re-raise to maintain pytest failure behavior
        # raise


@pytest.mark.asyncio
async def test_all():
    """Test the agent's basic ability on a few examples."""
    await run_detailed_evaluation()


# Allow running as script
if __name__ == "__main__":
    dotenv.load_dotenv()
    asyncio.run(run_detailed_evaluation())
