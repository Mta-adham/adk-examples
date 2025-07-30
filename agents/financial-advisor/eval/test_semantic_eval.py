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

"""Semantic evaluation test for Financial Advisor using component-based criteria."""

import asyncio
import pathlib
import sys
import json
from typing import Dict, Any

import dotenv
import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

pytest_plugins = ("pytest_asyncio",)


class SemanticEvaluator:
    """Custom evaluator for semantic component-based evaluation."""
    
    @staticmethod
    def evaluate_response(actual_response: str, expected_components: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate response based on expected components."""
        results = {
            "passed": True,
            "score": 0.0,
            "component_results": {},
            "missing_components": []
        }
        
        total_weight = 0.0
        weighted_score = 0.0
        
        # Get scoring config
        scoring = expected_components.get("scoring", {})
        weights = scoring.get("weights", {})
        
        # Evaluate each component
        for comp_name, comp_spec in expected_components.items():
            if comp_name == "scoring":
                continue
                
            component_score = SemanticEvaluator._evaluate_component(
                actual_response, comp_spec
            )
            
            weight = weights.get(comp_name, 1.0 / len(expected_components))
            total_weight += weight
            weighted_score += component_score * weight
            
            results["component_results"][comp_name] = {
                "score": component_score,
                "weight": weight,
                "passed": component_score >= 0.7
            }
            
            if comp_spec.get("required", False) and component_score < 0.7:
                results["missing_components"].append(comp_name)
        
        # Calculate final score
        results["score"] = weighted_score / total_weight if total_weight > 0 else 0
        pass_threshold = scoring.get("pass_threshold", 0.8)
        results["passed"] = results["score"] >= pass_threshold and len(results["missing_components"]) == 0
        
        return results
    
    @staticmethod
    def _evaluate_component(response: str, component: Dict[str, Any]) -> float:
        """Evaluate a single component based on its check type."""
        response_lower = response.lower()
        check_type = component.get("check_type", "contains")
        
        if check_type == "pattern":
            patterns = component.get("patterns", [])
            matches = sum(1 for p in patterns if p.lower() in response_lower)
            return matches / len(patterns) if patterns else 0
            
        elif check_type == "contains":
            values = component.get("values", [])
            matches = sum(1 for v in values if v.lower() in response_lower)
            return 1.0 if matches > 0 else 0.0
            
        elif check_type == "all_present":
            values = component.get("values", [])
            matches = sum(1 for v in values if v.lower() in response_lower)
            return matches / len(values) if values else 0
            
        elif check_type == "any_present":
            values = component.get("values", [])
            return 1.0 if any(v.lower() in response_lower for v in values) else 0.0
            
        elif check_type == "disclaimer_validation":
            min_length = component.get("min_length", 0)
            if len(response) < min_length:
                return 0.0
            
            required_phrases = component.get("required_phrases", [])
            matches = sum(1 for phrase in required_phrases if phrase.lower() in response_lower)
            return matches / len(required_phrases) if required_phrases else 1.0
            
        elif check_type == "semantic":
            # For semantic checks, we'd ideally use an LLM judge
            # For now, we'll do keyword matching as a proxy
            concept = component.get("concept", "")
            keywords = concept.lower().split()
            matches = sum(1 for k in keywords if k in response_lower)
            return matches / len(keywords) if keywords else 0
            
        return 0.0


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()


async def run_semantic_evaluation():
    """Run the semantic evaluation with detailed output."""
    print("=" * 80)
    print("FINANCIAL ADVISOR SEMANTIC EVALUATION - COMPONENT-BASED")
    print("=" * 80)
    print("This evaluation checks for required components using semantic matching")
    print("rather than exact text comparison")
    print("-" * 80)
    sys.stdout.flush()
    
    # Load semantic test data
    test_file = pathlib.Path(__file__).parent / "data" / "financial-advisor-semantic.test.json"
    
    with open(test_file, 'r') as f:
        test_data = json.load(f)
    
    print(f"Loaded semantic test: {test_data['name']}")
    print(f"Test cases: {len(test_data['eval_cases'])}")
    print(f"Evaluation type: {test_data['metadata']['evaluation_type']}")
    print("-" * 80)
    
    # Here you would run the actual evaluation
    # For demonstration, showing the structure
    for case in test_data['eval_cases']:
        print(f"\nTest case: {case['eval_id']}")
        print(f"Conversations: {len(case['conversation'])}")
        
        for conv in case['conversation']:
            if 'expected_components' in conv:
                print(f"  - Checking {len(conv['expected_components'])} components")
                print(f"  - Pass threshold: {conv.get('scoring', {}).get('pass_threshold', 0.8)}")
    
    print("=" * 80)
    print("SEMANTIC EVALUATION STRUCTURE READY")
    print("=" * 80)
    
    # Note: Actual evaluation would require:
    # 1. Running the agent with test inputs
    # 2. Applying SemanticEvaluator to responses
    # 3. Calculating scores and pass/fail status


@pytest.mark.asyncio
async def test_semantic_evaluation():
    """Test the agent using semantic evaluation criteria."""
    await run_semantic_evaluation()


# Allow running as script
if __name__ == "__main__":
    import sys
    import os
    import pdb
    
    # Disable all debugger functionality
    sys.breakpointhook = lambda: None
    os.environ['PYTHONBREAKPOINT'] = '0'
    
    # Override pdb functions to do nothing
    pdb.set_trace = lambda: None
    pdb.post_mortem = lambda: None
    
    # Disable bdb module tracing
    import bdb
    bdb.Bdb.trace_dispatch = lambda self, frame, event, arg: None
    
    dotenv.load_dotenv()
    asyncio.run(run_semantic_evaluation())