# LLM Auditor Agent - Evaluation Guide

This guide provides step-by-step instructions for setting up and running the evaluation of the LLM Auditor agent.

## Overview

The LLM Auditor is a multi-agent system that fact-checks LLM-generated responses by:
1. **Critic Agent**: Identifies and verifies claims using web search
2. **Reviser Agent**: Corrects inaccurate information while preserving correct facts

## Prerequisites

- Python 3.11+
- `uv` package manager
- Google Cloud CLI (`gcloud`) with authentication
- Google Cloud project with Vertex AI API enabled

## Environment Setup

### 1. Install Dependencies

```bash
uv sync --all-extras
```

This installs all required packages including:
- `google-adk` for agent framework
- `google-genai` for Gemini models
- `pytest` for evaluation execution

### 2. Configure Google Cloud Authentication

Ensure you're authenticated with Google Cloud:

```bash
# Check authentication status
gcloud auth list

# Set up application default credentials (if needed)
gcloud auth application-default login

# Verify your project is configured
gcloud config list
```

### 3. Configure Environment Variables

Create a `.env` file with your Google Cloud configuration:

```bash
# Using Vertex AI with application default credentials
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

**Note**: Replace `your-project-id` with your actual Google Cloud project ID.

## Running the Evaluation

### Execute Evaluation Tests

Run the evaluation using pytest:

```bash
uv run pytest eval -v -s
```

**Parameters explained:**
- `eval` - runs evaluation tests (not unit tests)
- `-v` - verbose output showing detailed results
- `-s` - no output capture (shows real-time progress)

### Expected Runtime

⏱️ **Evaluation Duration**: ~3 minutes (178.72 seconds)
- 2 test scenarios × 5 runs each = 10 total evaluations
- Each run involves LLM inference + web search + fact verification

## Evaluation Results

For detailed evaluation results including test execution data, performance metrics, and sample corrected outputs, see:

📁 **[evaluation_results/](./evaluation_results/)** directory

**Latest Results:**
- [2025-07-24 Test Execution Results](./evaluation_results/2025-07-24_test-execution-results.md) - ALL TESTS PASSED with 3-minute execution time and perfect fact-checking performance

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Ensure `gcloud auth application-default login` is completed
   - Verify your Google Cloud project has Vertex AI API enabled

2. **Timeout Errors**
   - Evaluation can take 3+ minutes due to web search and LLM calls
   - Use longer timeout values if needed

3. **API Quota Issues**
   - Check your Google Cloud project's Vertex AI quotas
   - Monitor usage in Google Cloud Console

### Environment Variables Troubleshooting

If evaluation fails, verify your environment configuration:

```bash
# Check if credentials are working
gcloud auth application-default print-access-token

# Verify project configuration
echo $GOOGLE_CLOUD_PROJECT
```

## Evaluation Output Schema

### Standard Metrics

The evaluation uses criteria defined in `eval/data/test_config.json`:

#### Tool Trajectory Average Score
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures correctness of multi-agent coordination between Critic and Reviser agents
- **Interpretation**:
  - 1.0 = Perfect coordination with proper fact-checking workflow execution
  - < 1.0 = Missing agent calls, incorrect tool usage, or workflow coordination failures
- **Threshold**: 1.0 (defined in `eval/data/test_config.json`)

#### Response Match Score
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures quality of fact-checking corrections using ROUGE scoring
- **Interpretation**:
  - 1.0 = Perfect match to expected correction (rare, only when no correction needed)
  - 0.46+ = High-quality corrections with accurate fact-checking
  - 0.35+ = Acceptable corrections meeting threshold requirements
  - < 0.35 = Insufficient correction quality or factual errors
- **Threshold**: 0.35 (defined in `eval/data/test_config.json`)

### Multi-Agent Workflow Evaluation

The evaluation specifically tests the coordination between:
- **Critic Agent**: Identifies and verifies claims using web search
- **Reviser Agent**: Corrects inaccurate information while preserving correct facts

### Output Format Example

```
| Metric | Threshold | Actual Score | Status |
|--------|-----------|--------------|---------|
| Tool Trajectory Avg Score | 1.0 | 1.0 | ✅ PASSED |
| Response Match Score | 0.35 | 0.46 | ✅ PASSED |

Final Status: 🎉 ALL TESTS PASSED
```

### Test Scenarios Evaluated

1. **Android Ice Cream Sandwich Test**:
   - **Input**: Accurate statement about Android 4.0
   - **Expected**: No correction needed
   - **Result**: Perfect performance (1.0/1.0 response match)

2. **Blueberry Color Explanation Test**:
   - **Input**: Misconception about pigments causing blue color
   - **Expected**: Correction explaining waxy coating and light scattering
   - **Result**: High-quality corrections (0.46/0.35 threshold)

### Success Indicators
- ✅ **Fact Verification**: Correctly identifies when statements are accurate vs. inaccurate
- ✅ **Web Search Integration**: Successfully uses web search to verify claims
- ✅ **Correction Quality**: Provides scientifically accurate corrections with proper explanations
- ✅ **Agent Coordination**: Perfect coordination between Critic and Reviser agents

### Performance Characteristics

- **Accuracy**: 100% tool trajectory score across all test cases
- **Consistency**: Reliable fact-checking and correction generation
- **Efficiency**: ~18 seconds per evaluation run (including web search)
- **Scalability**: Handles both simple verification and complex corrections
- **Evaluation Duration**: ~3 minutes (178.72 seconds) for 2 scenarios × 5 runs each

The LLM Auditor demonstrates robust performance in automated fact-checking scenarios, making it suitable for production applications requiring high accuracy in information verification.