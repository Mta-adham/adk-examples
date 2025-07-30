#!/usr/bin/env python3
"""Flexible semantic evaluation that's more forgiving of variations in agent responses."""

import asyncio
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple

import dotenv

dotenv.load_dotenv()


class FlexibleSemanticEvaluator:
    """More flexible evaluation that focuses on intent rather than exact patterns."""
    
    def __init__(self):
        self.introduction_criteria = {
            "greeting": {
                "intent": "Greets the user",
                "flexible_patterns": [
                    r"hello", r"hi\b", r"greetings", r"welcome",
                    r"good\s+(morning|afternoon|evening|day)"
                ],
                "weight": 0.10,
                "required": False  # Not strictly required if tone is professional
            },
            "identity": {
                "intent": "Identifies as Cymbal Financial Advisor",
                "flexible_patterns": [
                    r"cymbal\s+financial\s+advisor",
                    r"financial\s+advisor.*cymbal",
                    r"cymbal.*advisor",
                    r"with\s+cymbal"
                ],
                "weight": 0.15,
                "required": True
            },
            "purpose": {
                "intent": "Explains purpose of providing financial advice",
                "flexible_patterns": [
                    r"financial\s+advice",
                    r"help.*financial",
                    r"guide.*investment",
                    r"provide.*advice",
                    r"assist.*financial"
                ],
                "weight": 0.15,
                "required": True
            },
            "process_mention": {
                "intent": "Mentions structured process or steps",
                "flexible_patterns": [
                    r"structured\s+process",
                    r"step.*process",
                    r"analyze.*develop.*execute.*evaluat",
                    r"market.*trading.*execution.*risk",
                    r"four.*areas"
                ],
                "weight": 0.15,
                "required": True
            },
            "markdown_option": {
                "intent": "Mentions ability to show detailed results",
                "flexible_patterns": [
                    r"markdown",
                    r"detailed\s+result",
                    r"show.*detail",
                    r"request.*detail",
                    r"ask.*detail"
                ],
                "weight": 0.10,
                "required": False
            },
            "engagement": {
                "intent": "Asks if user is ready or engages them",
                "flexible_patterns": [
                    r"ready.*start",
                    r"ready.*get\s+started",
                    r"ready.*begin",
                    r"shall\s+we",
                    r"let.*start",
                    r"would\s+you\s+like"
                ],
                "weight": 0.10,
                "required": True
            },
            "disclaimer_present": {
                "intent": "Includes disclaimer about educational purposes",
                "flexible_patterns": [
                    r"educational.*informational.*purposes",
                    r"not.*constitute.*advice",
                    r"disclaimer",
                    r"your\s+own\s+risk",
                    r"consult.*advisor"
                ],
                "min_keywords": 3,  # Must have at least 3 disclaimer keywords
                "weight": 0.25,
                "required": True
            }
        }
        
        self.step_criteria = {
            "step_announcement": {
                "intent": "Announces moving to next step",
                "flexible_patterns": [
                    r"let.*begin",
                    r"let.*start",
                    r"first\s+step",
                    r"step\s+1",
                    r"market\s+data\s+analysis",
                    r"now.*move",
                    r"proceed.*to"
                ],
                "weight": 0.30,
                "required": True
            },
            "subagent_mention": {
                "intent": "Mentions using a subagent",
                "flexible_patterns": [
                    r"data_analyst",
                    r"data\s+analyst",
                    r"subagent",
                    r"I'll\s+call",
                    r"I'll\s+use",
                    r"help.*with\s+this"
                ],
                "weight": 0.30,
                "required": True
            },
            "ticker_request": {
                "intent": "Asks for ticker symbol",
                "flexible_patterns": [
                    r"ticker\s+symbol",
                    r"market\s+ticker",
                    r"provide.*ticker",
                    r"which.*ticker",
                    r"stock.*symbol"
                ],
                "weight": 0.20,
                "required": True
            },
            "examples": {
                "intent": "Provides example tickers",
                "flexible_patterns": [
                    r"AAPL",
                    r"GOOGL", 
                    r"MSFT",
                    r"example",
                    r"e\.g\.",
                    r"such\s+as"
                ],
                "weight": 0.20,
                "required": False
            }
        }
        
        self.disclaimer_keywords = [
            "educational", "informational", "purposes", "not constitute",
            "financial advice", "no warranty", "no representations",
            "your own risk", "consult", "qualified", "advisor",
            "not an offer", "investment decisions", "AI model",
            "generated", "should not be interpreted"
        ]
    
    def evaluate_introduction(self, response: str) -> Dict[str, Any]:
        """Evaluate introduction with flexible criteria."""
        return self._evaluate_against_criteria(response, self.introduction_criteria, "introduction")
    
    def evaluate_step_progression(self, response: str) -> Dict[str, Any]:
        """Evaluate step progression with flexible criteria."""
        return self._evaluate_against_criteria(response, self.step_criteria, "step_progression")
    
    def _evaluate_against_criteria(self, response: str, criteria: Dict, eval_type: str) -> Dict[str, Any]:
        """Evaluate response against flexible criteria."""
        response_lower = response.lower()
        
        results = {
            "overall_score": 0.0,
            "criteria_scores": {},
            "criteria_met": {},
            "missing_criteria": [],
            "passed": False,
            "eval_type": eval_type
        }
        
        total_weight = 0.0
        weighted_score = 0.0
        
        for criterion_name, criterion_spec in criteria.items():
            score = self._score_criterion(response_lower, criterion_spec)
            
            results["criteria_scores"][criterion_name] = {
                "score": score,
                "intent": criterion_spec["intent"],
                "met": score >= 0.7,
                "required": criterion_spec.get("required", True)
            }
            
            if score >= 0.7:
                results["criteria_met"][criterion_name] = True
            elif criterion_spec.get("required", True):
                results["missing_criteria"].append({
                    "name": criterion_name,
                    "intent": criterion_spec["intent"],
                    "score": score
                })
            
            weight = criterion_spec.get("weight", 0.1)
            total_weight += weight
            weighted_score += score * weight
        
        # Calculate overall score
        results["overall_score"] = weighted_score / total_weight if total_weight > 0 else 0
        
        # Determine if passed (more lenient: 0.75 threshold)
        required_met = all(
            results["criteria_scores"][name]["met"] 
            for name, spec in criteria.items() 
            if spec.get("required", True)
        )
        results["passed"] = required_met and results["overall_score"] >= 0.75
        
        # Add detailed feedback
        results["feedback"] = self._generate_feedback(results, criteria)
        
        return results
    
    def _score_criterion(self, response_lower: str, criterion_spec: Dict) -> float:
        """Score a single criterion with flexibility."""
        patterns = criterion_spec.get("flexible_patterns", [])
        
        if not patterns and "min_keywords" in criterion_spec:
            # Special handling for keyword-based criteria (like disclaimer)
            return self._score_keywords(response_lower, criterion_spec)
        
        # Score based on pattern matching
        scores = []
        for pattern in patterns:
            if re.search(pattern, response_lower, re.IGNORECASE):
                # Full match gets higher score
                if pattern in response_lower:
                    scores.append(1.0)
                else:
                    scores.append(0.85)  # Regex match but not exact
        
        if not scores:
            # Check for semantic similarity to intent
            intent_score = self._check_intent_similarity(response_lower, criterion_spec["intent"])
            scores.append(intent_score)
        
        return max(scores) if scores else 0.0
    
    def _score_keywords(self, response_lower: str, criterion_spec: Dict) -> float:
        """Score based on keyword presence."""
        keyword_count = 0
        
        for keyword in self.disclaimer_keywords:
            if keyword.lower() in response_lower:
                keyword_count += 1
        
        min_keywords = criterion_spec.get("min_keywords", 3)
        
        # Score based on how many keywords found
        if keyword_count >= min_keywords * 2:
            return 1.0
        elif keyword_count >= min_keywords:
            return 0.8 + (0.2 * (keyword_count - min_keywords) / min_keywords)
        else:
            return keyword_count / min_keywords * 0.7
    
    def _check_intent_similarity(self, response_lower: str, intent: str) -> float:
        """Basic intent matching without LLM."""
        intent_keywords = {
            "Greets the user": ["hello", "hi", "welcome", "greet"],
            "Identifies as Cymbal Financial Advisor": ["cymbal", "financial", "advisor"],
            "Explains purpose of providing financial advice": ["help", "assist", "guide", "advice", "financial"],
            "Mentions structured process or steps": ["process", "step", "structure", "analyze", "evaluate"],
            "Mentions ability to show detailed results": ["detail", "markdown", "show", "result"],
            "Asks if user is ready or engages them": ["ready", "start", "begin", "shall"],
            "Includes disclaimer about educational purposes": ["educational", "risk", "not advice", "disclaimer"],
            "Announces moving to next step": ["begin", "start", "step", "first", "proceed"],
            "Mentions using a subagent": ["analyst", "subagent", "agent", "help"],
            "Asks for ticker symbol": ["ticker", "symbol", "provide", "which"],
            "Provides example tickers": ["example", "aapl", "googl", "msft", "e.g."]
        }
        
        keywords = intent_keywords.get(intent, intent.lower().split())
        matches = sum(1 for kw in keywords if kw in response_lower)
        
        return min(matches / len(keywords) if keywords else 0, 0.6)  # Cap at 0.6 for intent matching
    
    def _generate_feedback(self, results: Dict, criteria: Dict) -> List[str]:
        """Generate helpful feedback."""
        feedback = []
        
        if results["passed"]:
            feedback.append(f"✅ Response meets requirements (score: {results['overall_score']:.3f})")
        else:
            feedback.append(f"❌ Response needs improvement (score: {results['overall_score']:.3f})")
        
        # Highlight what's working
        met_criteria = [name for name, met in results["criteria_met"].items() if met]
        if met_criteria:
            feedback.append(f"✓ Successfully includes: {', '.join(met_criteria)}")
        
        # Point out missing required elements
        if results["missing_criteria"]:
            missing_names = [m["name"] for m in results["missing_criteria"]]
            feedback.append(f"✗ Missing required elements: {', '.join(missing_names)}")
        
        return feedback


async def run_flexible_evaluation():
    """Run flexible semantic evaluation on agent."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    from google.adk.runners import InMemoryRunner
    from google.genai.types import Part, UserContent
    from financial_advisor.agent import root_agent
    
    evaluator = FlexibleSemanticEvaluator()
    
    print("=" * 80)
    print("FLEXIBLE SEMANTIC EVALUATION")
    print("=" * 80)
    print("Evaluating agent responses with focus on intent and flexibility...")
    print("-" * 80)
    
    # Initialize runner
    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id="flexible_eval_user"
    )
    
    test_cases = [
        {
            "input": "Hello. What can you do for me?",
            "eval_func": evaluator.evaluate_introduction,
            "description": "Initial greeting"
        },
        {
            "input": "Yes please.",
            "eval_func": evaluator.evaluate_step_progression,
            "description": "User agrees to start"
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTEST {i}: {test['description']}")
        print("=" * 60)
        
        # Get agent response
        content = UserContent(parts=[Part(text=test["input"])])
        response = ""
        
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                response = event.content.parts[0].text
        
        # Evaluate
        eval_result = test["eval_func"](response)
        eval_result["test_description"] = test["description"]
        eval_result["user_input"] = test["input"]
        eval_result["agent_response"] = response
        
        # Display results
        print(f"Score: {eval_result['overall_score']:.3f} - {'PASSED' if eval_result['passed'] else 'FAILED'}")
        
        print("\nCriteria Scores:")
        for name, data in eval_result["criteria_scores"].items():
            status = "✓" if data["met"] else "✗"
            req = " (required)" if data["required"] else ""
            print(f"  {status} {name}: {data['score']:.3f} - {data['intent']}{req}")
        
        print("\nFeedback:")
        for fb in eval_result["feedback"]:
            print(f"  {fb}")
        
        results.append(eval_result)
    
    # Summary
    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)
    
    avg_score = sum(r["overall_score"] for r in results) / len(results)
    passed = sum(1 for r in results if r["passed"])
    
    print(f"Average Score: {avg_score:.3f}")
    print(f"Tests Passed: {passed}/{len(results)}")
    
    # Save results
    output_file = Path(__file__).parent / "flexible_evaluation_results.json"
    with open(output_file, "w") as f:
        json.dump({
            "evaluator": "Flexible Semantic Evaluator",
            "results": results,
            "summary": {
                "average_score": avg_score,
                "tests_passed": passed,
                "total_tests": len(results)
            }
        }, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    import os
    import sys
    
    sys.breakpointhook = lambda: None
    os.environ['PYTHONBREAKPOINT'] = '0'
    
    asyncio.run(run_flexible_evaluation())