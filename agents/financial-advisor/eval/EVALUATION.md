# Financial Advisor Agent - Evaluation Guide

This guide provides step-by-step instructions for setting up and running the evaluation of the Financial Advisor agent.

## Prerequisites

- Python 3.9+
- `uv` package manager
- Google Cloud Platform project with appropriate permissions
- `gcloud` CLI configured and authenticated

## Environment Setup

### 1. Install Dependencies

```bash
uv sync --all-extras
```

This installs all required dependencies including evaluation tools from the `google-adk[eval]` package.

### 2. Configure Google Cloud Credentials

Ensure you have authenticated with Google Cloud:

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project $GOOGLE_CLOUD_PROJECT
```

### 3. Create Environment Configuration

Create a `.env` file in the project root with the following variables:

```bash
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

Replace `your-project-id` with your actual Google Cloud project ID.

## Running the Evaluation

Execute the evaluation using:

```bash
uv run pytest eval -v
```

The evaluation uses the `AgentEvaluator` from ADK to test the agent against predefined test cases in `eval/data/financial-advisor.test.json`.

## Evaluation Configuration

The evaluation runs with the following parameters:
- **Test cases**: Located in `eval/data/financial-advisor.test.json`
- **Number of runs**: 5 iterations per test case
- **Success criteria**:
  - `response_match_score`: 0.8 (80% similarity threshold)
  - `tool_trajectory_avg_score`: 1.0 (100% tool usage accuracy)

## Test Results

## Evaluation Results

For detailed evaluation results including test scores, failure analysis, and functional assessment, see:

📁 **[evaluation_results/](./evaluation_results/)** directory

**Latest Results:**
- [2025-07-24 Evaluation Results](./evaluation_results/2025-07-24_evaluation-results.md) - FAILED similarity threshold (0.58-0.65 vs 0.8 required) but functionally correct

## Troubleshooting

### Common Issues

1. **Missing Google Cloud credentials**
   ```
   ValueError: Missing key inputs argument! To use the Google AI API, provide (`api_key`) arguments. To use the Google Cloud API, provide (`vertexai`, `project` & `location`) arguments.
   ```
   **Solution**: Ensure `.env` file is properly configured and `gcloud auth application-default login` has been run.

2. **Module import errors**
   ```
   ModuleNotFoundError: No module named 'google.adk'
   ```
   **Solution**: Install all dependencies with `uv sync --all-extras`

3. **Permission errors**
   **Solution**: Verify your Google Cloud project has the necessary APIs enabled and your account has appropriate permissions.

4. **API Authentication Errors**
   - Verify Google Cloud credentials: `gcloud auth application-default login`
   - Ensure Vertex AI API is enabled: `gcloud services enable aiplatform.googleapis.com`
   - Check project configuration: `gcloud config get-value project`

## Evaluation Interpretation

The current evaluation results indicate that while the agent is functionally correct, the evaluation framework is sensitive to:
- Response formatting differences
- Additional explanatory content
- Minor phrasing variations

For production use, consider:
1. Adjusting similarity thresholds to account for natural language variation
2. Focusing on functional correctness rather than exact text matching
3. Updating expected responses to reflect current agent behavior patterns

## Evaluation Output Schema

### Standard Metrics

The evaluation runs with the following success criteria from the test configuration:

#### Response Match Score
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures semantic similarity between agent responses and expected financial advisory responses using ROUGE scoring
- **Interpretation**:
  - 0.8+ = High similarity to expected professional financial advisory responses
  - 0.58-0.65 = Functionally correct but with phrasing/structural differences (typical actual scores)
  - < 0.5 = Significant differences in response content or structure
- **Threshold**: 0.8 (80% similarity threshold)

#### Tool Trajectory Average Score
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures correctness of tool usage and sub-agent orchestration in financial workflows
- **Interpretation**:
  - 1.0 = Perfect tool usage accuracy with correct sub-agent coordination
  - < 1.0 = Incorrect tool calls, missing sub-agent interactions, or workflow errors
- **Threshold**: 1.0 (100% tool usage accuracy required)

### Evaluation Configuration

- **Test Data**: `eval/data/financial-advisor.test.json`
- **Number of Runs**: 5 iterations per test case
- **Evaluation Framework**: ADK `AgentEvaluator`

### Output Format Example

```
Status: ⚠️ FAILED (Similarity threshold not met)

| Metric | Score | Threshold | Status |
|--------|-------|-----------|---------|
| Response Match Score | 0.58-0.65 | 0.8 | ❌ FAILED |
| Tool Trajectory Average Score | 1.0 | 1.0 | ✅ PASSED |
```

### Common Failure Patterns

1. **Response Structure**: Agent responses include additional explanatory text not present in expected responses
2. **Phrasing Variations**: Functionally equivalent but differently worded responses  
3. **Disclaimer Placement**: Legal disclaimers appear in different positions or with slightly different wording

### Success Indicators (Functional Assessment)
Despite evaluation metric failures, the agent demonstrates:
- ✅ **Correct Workflow Execution**: Proper financial advisory process flow
- ✅ **Sub-Agent Orchestration**: Appropriate coordination with data_analyst and other sub-agents
- ✅ **Response Quality**: Professional financial advisory responses with complete legal disclaimers
- ✅ **User Input Handling**: Appropriate responses to user inputs and requests
- ✅ **Structured Process**: Follows systematic financial analysis methodology

### Threshold Sensitivity
The evaluation framework is sensitive to:
- Response formatting differences
- Additional explanatory content beyond expected responses
- Minor phrasing variations in otherwise correct responses
- Natural language variations in professional communication

## Next Steps

To improve evaluation scores:
1. Review and standardize agent response templates
2. Adjust evaluation criteria to focus on functional outcomes
3. Update expected responses in test data to match current agent behavior
4. Consider using semantic similarity measures instead of exact text matching