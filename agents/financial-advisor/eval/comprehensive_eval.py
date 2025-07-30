#!/usr/bin/env python3
"""Comprehensive evaluation suite combining multiple evaluation methods."""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

import dotenv
from google.genai import Client
from google.genai.types import GenerateContentConfig, Part, UserContent

dotenv.load_dotenv()


class ComprehensiveEvaluator:
    """Combines multiple evaluation methods for thorough assessment."""
    
    def __init__(self):
        self.client = Client()
        self.evaluation_methods = {
            "llm_judge": self._llm_judge_eval,
            "structured_rubric": self._structured_rubric_eval,
            "comparative_eval": self._comparative_eval,
            "task_completion": self._task_completion_eval
        }
    
    async def evaluate_agent(self, test_cases: List[Dict[str, Any]], agent_runner) -> Dict[str, Any]:
        """Run comprehensive evaluation on agent with multiple methods."""
        
        results = {
            "test_cases": [],
            "method_scores": {},
            "overall_analysis": {}
        }
        
        for test_case in test_cases:
            case_results = await self._evaluate_single_case(test_case, agent_runner)
            results["test_cases"].append(case_results)
        
        # Aggregate scores by method
        for method in self.evaluation_methods:
            scores = [tc["evaluations"][method]["score"] 
                     for tc in results["test_cases"] 
                     if method in tc.get("evaluations", {})]
            if scores:
                results["method_scores"][method] = {
                    "average": sum(scores) / len(scores),
                    "min": min(scores),
                    "max": max(scores)
                }
        
        # Generate overall analysis
        results["overall_analysis"] = await self._generate_overall_analysis(results)
        
        return results
    
    async def _evaluate_single_case(self, test_case: Dict[str, Any], agent_runner) -> Dict[str, Any]:
        """Evaluate a single test case with all methods."""
        
        # Get agent response
        agent_response = await self._get_agent_response(
            test_case["input"], 
            agent_runner,
            test_case.get("context")
        )
        
        case_result = {
            "input": test_case["input"],
            "description": test_case.get("description", ""),
            "agent_response": agent_response,
            "evaluations": {}
        }
        
        # Run each evaluation method
        for method_name, method_func in self.evaluation_methods.items():
            try:
                eval_result = await method_func(test_case, agent_response)
                case_result["evaluations"][method_name] = eval_result
            except Exception as e:
                case_result["evaluations"][method_name] = {
                    "score": 0.0,
                    "error": str(e)
                }
        
        return case_result
    
    async def _get_agent_response(self, user_input: str, agent_runner, context: Optional[Dict] = None) -> str:
        """Get response from agent."""
        content = UserContent(parts=[Part(text=user_input)])
        response_text = ""
        
        async for event in agent_runner.run_async(
            user_id=context.get("user_id") if context else "eval_user",
            session_id=context.get("session_id") if context else None,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                response_text = event.content.parts[0].text
        
        return response_text
    
    async def _llm_judge_eval(self, test_case: Dict[str, Any], agent_response: str) -> Dict[str, Any]:
        """LLM-based evaluation focusing on quality and appropriateness."""
        
        prompt = f"""As an expert evaluator, assess this financial advisor response:

User Input: {test_case['input']}
Expected Type: {test_case.get('eval_type', 'general')}
Agent Response: {agent_response}

Evaluate on:
1. Appropriateness: Does the response fit the context and user need?
2. Completeness: Are all necessary elements included?
3. Clarity: Is the response clear and well-structured?
4. Professionalism: Does it maintain appropriate tone?
5. Accuracy: Is the information correct and reliable?

Provide a score (0-1) and detailed feedback.

Respond in JSON format:
{{
  "score": <0-1>,
  "dimensions": {{
    "appropriateness": <0-1>,
    "completeness": <0-1>,
    "clarity": <0-1>,
    "professionalism": <0-1>,
    "accuracy": <0-1>
  }},
  "feedback": "<detailed feedback>",
  "improvements": ["<suggestion1>", "<suggestion2>"]
}}"""

        response = await self.client.aio.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=GenerateContentConfig(temperature=0.1, response_mime_type="application/json")
        )
        
        return json.loads(response.text)
    
    async def _structured_rubric_eval(self, test_case: Dict[str, Any], agent_response: str) -> Dict[str, Any]:
        """Evaluation based on structured rubric criteria."""
        
        rubric = test_case.get("rubric", self._get_default_rubric(test_case.get("eval_type")))
        
        prompt = f"""Evaluate this response against a structured rubric:

User Input: {test_case['input']}
Agent Response: {agent_response}

Rubric Criteria:
{json.dumps(rubric, indent=2)}

For each criterion, provide:
- Score (0-1)
- Evidence from the response
- Missing elements

Respond in JSON format:
{{
  "score": <overall score 0-1>,
  "criteria_scores": {{
    "<criterion_name>": {{
      "score": <0-1>,
      "evidence": "<what was found>",
      "missing": "<what was missing>"
    }}
  }},
  "total_criteria_met": <number>,
  "total_criteria": <number>
}}"""

        response = await self.client.aio.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=GenerateContentConfig(temperature=0.1, response_mime_type="application/json")
        )
        
        return json.loads(response.text)
    
    async def _comparative_eval(self, test_case: Dict[str, Any], agent_response: str) -> Dict[str, Any]:
        """Compare response against ideal examples."""
        
        ideal_response = test_case.get("ideal_response", self._get_ideal_response(test_case.get("eval_type")))
        
        prompt = f"""Compare the agent response against an ideal response:

User Input: {test_case['input']}

IDEAL Response (for reference):
{ideal_response}

ACTUAL Agent Response:
{agent_response}

Compare on:
1. Content Coverage: Does it cover similar points?
2. Structure: Is it organized similarly well?
3. Tone Match: Does it maintain appropriate tone?
4. Key Elements: Are critical elements present?

Don't penalize for different wording, focus on semantic equivalence.

Respond in JSON format:
{{
  "score": <0-1>,
  "content_coverage": <0-1>,
  "structure_quality": <0-1>,
  "tone_match": <0-1>,
  "key_elements_present": ["<element1>", "<element2>"],
  "key_elements_missing": ["<element1>", "<element2>"],
  "overall_assessment": "<brief assessment>"
}}"""

        response = await self.client.aio.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=GenerateContentConfig(temperature=0.1, response_mime_type="application/json")
        )
        
        return json.loads(response.text)
    
    async def _task_completion_eval(self, test_case: Dict[str, Any], agent_response: str) -> Dict[str, Any]:
        """Evaluate if the response accomplishes the intended task."""
        
        task_goals = test_case.get("task_goals", self._get_task_goals(test_case.get("eval_type")))
        
        prompt = f"""Evaluate task completion:

User Input: {test_case['input']}
Agent Response: {agent_response}

Task Goals:
{json.dumps(task_goals, indent=2)}

For each goal, determine:
1. Is it achieved? (yes/no/partial)
2. How well? (0-1 score)
3. Evidence from response

Respond in JSON format:
{{
  "score": <overall 0-1>,
  "goals_achieved": <number>,
  "total_goals": <number>,
  "goal_evaluation": {{
    "<goal_name>": {{
      "achieved": "<yes/no/partial>",
      "score": <0-1>,
      "evidence": "<quote or description>"
    }}
  }},
  "task_success": <true/false>
}}"""

        response = await self.client.aio.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=GenerateContentConfig(temperature=0.1, response_mime_type="application/json")
        )
        
        return json.loads(response.text)
    
    def _get_default_rubric(self, eval_type: str) -> Dict[str, Any]:
        """Get default rubric for evaluation type."""
        rubrics = {
            "introduction": {
                "greeting": {"weight": 0.15, "description": "Professional greeting"},
                "identity": {"weight": 0.20, "description": "Clear identification as Cymbal Financial Advisor"},
                "purpose": {"weight": 0.20, "description": "Explains purpose and capabilities"},
                "process": {"weight": 0.15, "description": "Outlines the advisory process"},
                "engagement": {"weight": 0.10, "description": "Engages user to proceed"},
                "disclaimer": {"weight": 0.20, "description": "Includes appropriate disclaimer"}
            },
            "step_progression": {
                "acknowledgment": {"weight": 0.25, "description": "Acknowledges moving to next step"},
                "subagent": {"weight": 0.25, "description": "Mentions relevant subagent"},
                "instructions": {"weight": 0.25, "description": "Clear instructions for user"},
                "examples": {"weight": 0.25, "description": "Provides helpful examples"}
            }
        }
        return rubrics.get(eval_type, {})
    
    def _get_ideal_response(self, eval_type: str) -> str:
        """Get ideal response example for evaluation type."""
        ideal_responses = {
            "introduction": """Hello! I'm with Cymbal Financial Advisor, here to provide comprehensive financial advice through a structured process. We'll analyze market data, develop trading strategies, create execution plans, and evaluate risk. Remember you can always ask to show me the detailed result as markdown. Ready to get started?

Important Disclaimer: For Educational and Informational Purposes Only. The information and trading strategy outlines provided by this tool are generated by an AI model and are for educational and informational purposes only. They do not constitute financial advice, investment recommendations, or offers to buy or sell any securities. Google and its affiliates make no representations or warranties about the completeness, accuracy, or reliability of the information provided. Any reliance you place on such information is at your own risk. Investment decisions should not be made based solely on this information. Financial markets are subject to risks, and past performance is not indicative of future results. You should conduct your own research and consult with a qualified financial advisor before making any investment decisions.""",
            
            "step_progression": """Great! Let's begin with the first step: market data analysis. I'll call the data_analyst subagent to help with this. Please provide the market ticker symbol you'd like me to analyze - for example, AAPL, GOOGL, or MSFT."""
        }
        return ideal_responses.get(eval_type, "")
    
    def _get_task_goals(self, eval_type: str) -> List[Dict[str, str]]:
        """Get task goals for evaluation type."""
        task_goals = {
            "introduction": [
                {"name": "establish_identity", "description": "Clearly identify as financial advisor"},
                {"name": "explain_purpose", "description": "Explain what the agent can do"},
                {"name": "outline_process", "description": "Describe the advisory process"},
                {"name": "provide_disclaimer", "description": "Include legal/educational disclaimer"},
                {"name": "engage_user", "description": "Ask if user wants to proceed"}
            ],
            "step_progression": [
                {"name": "acknowledge_progress", "description": "Show movement to next step"},
                {"name": "identify_subagent", "description": "Mention which subagent will help"},
                {"name": "request_information", "description": "Ask for specific user input"},
                {"name": "provide_guidance", "description": "Give examples or guidance"}
            ]
        }
        return task_goals.get(eval_type, [])
    
    async def _generate_overall_analysis(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall analysis from all evaluation results."""
        
        prompt = f"""Analyze these comprehensive evaluation results:

{json.dumps(results, indent=2)}

Provide:
1. Overall assessment of agent performance
2. Consistent strengths across methods
3. Consistent weaknesses across methods
4. Specific recommendations for improvement
5. Overall grade (A-F) with justification

Respond in JSON format:
{{
  "overall_assessment": "<detailed assessment>",
  "consistent_strengths": ["<strength1>", "<strength2>"],
  "consistent_weaknesses": ["<weakness1>", "<weakness2>"],
  "recommendations": ["<rec1>", "<rec2>"],
  "grade": "<A-F>",
  "grade_justification": "<why this grade>",
  "improvement_priority": ["<highest priority>", "<second priority>"]
}}"""

        response = await self.client.aio.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=GenerateContentConfig(temperature=0.2, response_mime_type="application/json")
        )
        
        return json.loads(response.text)


async def main():
    """Run comprehensive evaluation."""
    
    # Import agent
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from google.adk.runners import InMemoryRunner
    from financial_advisor.agent import root_agent
    
    print("=" * 80)
    print("COMPREHENSIVE FINANCIAL ADVISOR EVALUATION")
    print("=" * 80)
    print("Running multiple evaluation methods for thorough assessment...")
    print("-" * 80)
    
    # Test cases
    test_cases = [
        {
            "input": "Hello. What can you do for me?",
            "eval_type": "introduction",
            "description": "Initial greeting and introduction"
        },
        {
            "input": "Yes please.",
            "eval_type": "step_progression",
            "description": "User agrees to start",
            "context": {"previous": "introduction"}
        }
    ]
    
    # Initialize
    evaluator = ComprehensiveEvaluator()
    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id="comprehensive_eval_user"
    )
    
    # Add session context to test cases
    for tc in test_cases:
        if "context" not in tc:
            tc["context"] = {}
        tc["context"]["session_id"] = session.id
        tc["context"]["user_id"] = session.user_id
    
    # Create a simple wrapper that matches expected interface
    class RunnerWrapper:
        def __init__(self, runner, session_id, user_id):
            self.runner = runner
            self.session_id = session_id
            self.user_id = user_id
            
        async def run_async(self, user_id, session_id, new_message):
            async for event in self.runner.run_async(
                user_id=user_id or self.user_id,
                session_id=session_id or self.session_id,
                new_message=new_message
            ):
                yield event
    
    wrapped_runner = RunnerWrapper(runner, session.id, session.user_id)
    
    # Run evaluation
    results = await evaluator.evaluate_agent(test_cases, wrapped_runner)
    
    # Display results
    for i, test_result in enumerate(results["test_cases"], 1):
        print(f"\nTEST CASE {i}: {test_result.get('description', 'Unknown')}")
        print("=" * 60)
        print(f"Input: {test_result['input']}")
        print("-" * 40)
        
        print("\nEvaluation Scores:")
        for method, eval_data in test_result["evaluations"].items():
            if "error" not in eval_data:
                print(f"  {method}: {eval_data.get('score', 0):.3f}")
        
        print("\nAgent Response Preview:")
        response = test_result['agent_response']
        print(response[:200] + "..." if len(response) > 200 else response)
    
    # Overall summary
    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)
    
    print("\nMethod Averages:")
    for method, scores in results["method_scores"].items():
        print(f"  {method}: {scores['average']:.3f} (min: {scores['min']:.3f}, max: {scores['max']:.3f})")
    
    analysis = results["overall_analysis"]
    print(f"\nOverall Grade: {analysis['grade']}")
    print(f"Justification: {analysis['grade_justification']}")
    
    print("\nConsistent Strengths:")
    for strength in analysis.get("consistent_strengths", []):
        print(f"  ✓ {strength}")
    
    print("\nConsistent Weaknesses:")
    for weakness in analysis.get("consistent_weaknesses", []):
        print(f"  ✗ {weakness}")
    
    print("\nImprovement Priorities:")
    for i, priority in enumerate(analysis.get("improvement_priority", []), 1):
        print(f"  {i}. {priority}")
    
    # Save results
    results_file = Path(__file__).parent / "comprehensive_evaluation_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: {results_file}")


if __name__ == "__main__":
    # Disable debugger
    sys.breakpointhook = lambda: None
    os.environ['PYTHONBREAKPOINT'] = '0'
    
    asyncio.run(main())