#!/usr/bin/env python3
"""Run semantic evaluation against actual Financial Advisor agent responses."""

import asyncio
import json
import sys
import os
from pathlib import Path

# Add parent directory to path to import agent
sys.path.insert(0, str(Path(__file__).parent.parent))

import dotenv
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent
from financial_advisor.agent import root_agent
from semantic_eval import evaluate_introduction, evaluate_step_progression, calculate_overall_semantic_score

dotenv.load_dotenv()


async def run_agent_and_get_response(user_input: str, session_id: str = None, runner: InMemoryRunner = None, user_id: str = None) -> tuple[str, InMemoryRunner, str, str]:
    """Run the financial advisor agent and get its response."""
    
    # Create runner and session if not provided
    if runner is None:
        runner = InMemoryRunner(agent=root_agent)
    
    if session_id is None:
        session = await runner.session_service.create_session(
            app_name=runner.app_name, 
            user_id="eval_user"
        )
        session_id = session.id
        user_id = session.user_id
    
    # Create user content
    content = UserContent(parts=[Part(text=user_input)])
    
    # Run agent and collect response
    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            response_text = event.content.parts[0].text
    
    return response_text, runner, session_id, user_id


async def evaluate_agent_response(agent_response: str, eval_type: str = "introduction"):
    """Evaluate a single agent response and display metrics."""
    
    print("=" * 80)
    print(f"EVALUATING {eval_type.upper()} RESPONSE")
    print("=" * 80)
    print("\nResponse preview:")
    print("-" * 40)
    print(agent_response[:300] + "..." if len(agent_response) > 300 else agent_response)
    print("-" * 40)
    
    if eval_type == "introduction":
        results = evaluate_introduction(agent_response)
    elif eval_type == "step1":
        results = evaluate_step_progression(agent_response, "step1_data_analysis")
    else:
        # Generic semantic evaluation
        results = calculate_overall_semantic_score(agent_response)
    
    # Display comprehensive metrics
    print(f"\n📊 EVALUATION METRICS:")
    print(f"Overall Score: {results.get('overall_score', 0):.3f}")
    print(f"Status: {'✅ PASSED' if results.get('passed', False) else '❌ FAILED'}")
    
    if 'detailed_scores' in results:
        print(f"\n📈 Category Scores:")
        for category, score in results['detailed_scores'].items():
            if isinstance(score, (int, float)):
                print(f"  - {category}: {score:.3f}")
    
    if 'component_breakdown' in results:
        print(f"\n🔍 Component Analysis:")
        for comp_name, comp_data in results['component_breakdown'].items():
            status = '✓' if comp_data.get('present', False) else '✗'
            score = comp_data.get('score', 0)
            print(f"  - {comp_name}: {score:.3f} {status}")
    
    if 'missing_components' in results:
        print(f"\n⚠️  Missing Components:")
        for missing in results['missing_components']:
            if isinstance(missing, dict):
                print(f"  - {missing['component']}: {missing['description']}")
            else:
                print(f"  - {missing}")
    
    if 'summary' in results:
        summary = results['summary']
        print(f"\n📋 Summary:")
        print(f"  - Total Components: {summary.get('total_components', 0)}")
        print(f"  - Passed Components: {summary.get('passed_components', 0)}")
        print(f"  - Average Score: {summary.get('average_component_score', 0):.3f}")
    
    return results


async def main():
    """Main evaluation runner - runs actual agent and evaluates responses."""
    
    print("=" * 80)
    print("FINANCIAL ADVISOR SEMANTIC EVALUATION - LIVE AGENT TEST")
    print("=" * 80)
    print("Running actual financial advisor agent and evaluating responses...")
    print("-" * 80)
    
    # Test conversation flow
    test_conversations = [
        {
            "input": "Hello. What can you do for me?",
            "eval_type": "introduction",
            "description": "Initial greeting and introduction"
        },
        {
            "input": "Yes please.",
            "eval_type": "step1",
            "description": "User agrees to start"
        }
    ]
    
    runner = None
    session_id = None
    user_id = None
    overall_results = []
    
    for i, test_case in enumerate(test_conversations, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}: {test_case['description']}")
        print(f"{'='*80}")
        print(f"User Input: '{test_case['input']}'")
        print("-" * 40)
        
        # Run agent
        print("Running agent...")
        response, runner, session_id, user_id = await run_agent_and_get_response(
            test_case['input'], 
            session_id, 
            runner,
            user_id
        )
        
        # Evaluate response
        results = await evaluate_agent_response(response, test_case['eval_type'])
        results['test_case'] = test_case['description']
        overall_results.append(results)
        
        # Brief pause for readability
        await asyncio.sleep(0.5)
    
    # Overall summary
    print("\n" + "=" * 80)
    print("OVERALL EVALUATION SUMMARY")
    print("=" * 80)
    
    total_score = sum(r.get('overall_score', 0) for r in overall_results)
    avg_score = total_score / len(overall_results) if overall_results else 0
    
    print(f"Total Test Cases: {len(overall_results)}")
    print(f"Average Score: {avg_score:.3f}")
    print(f"Overall Status: {'✅ PASSED' if avg_score >= 0.8 else '❌ FAILED'}")
    
    print("\nIndividual Test Results:")
    for result in overall_results:
        status = '✅' if result.get('passed', False) else '❌'
        print(f"  - {result['test_case']}: {result.get('overall_score', 0):.3f} {status}")
    
    # Grade assignment
    if avg_score >= 0.9:
        grade = 'A'
        feedback = "Excellent! Agent responses meet all requirements with high quality."
    elif avg_score >= 0.8:
        grade = 'B'
        feedback = "Good performance. Minor improvements could enhance response quality."
    elif avg_score >= 0.7:
        grade = 'C'
        feedback = "Acceptable but needs improvement in several areas."
    elif avg_score >= 0.6:
        grade = 'D'
        feedback = "Below expectations. Significant improvements needed."
    else:
        grade = 'F'
        feedback = "Failing. Major revisions required to meet basic requirements."
    
    print(f"\nFinal Grade: {grade}")
    print(f"Feedback: {feedback}")
    
    # Save results
    results_file = Path(__file__).parent / "semantic_evaluation_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "overall_results": overall_results,
            "summary": {
                "average_score": avg_score,
                "grade": grade,
                "feedback": feedback,
                "test_count": len(overall_results)
            }
        }, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")


if __name__ == "__main__":
    # Disable debugger
    sys.breakpointhook = lambda: None
    os.environ['PYTHONBREAKPOINT'] = '0'
    
    import pdb
    pdb.set_trace = lambda: None
    
    asyncio.run(main())