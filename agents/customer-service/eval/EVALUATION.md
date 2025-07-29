# Customer Service Agent Evaluation Guide

This guide provides instructions for setting up and running the evaluation tests for the Cymbal Home & Garden Customer Service Agent.

## Overview

The Customer Service Agent is an AI-powered assistant built using Google's Agent Development Kit (ADK). It provides personalized customer service including product recommendations, order management, appointment scheduling, and customer support through a comprehensive set of tools.

## Prerequisites

- Python 3.11+
- uv (for dependency management)
- Google Cloud Project with Vertex AI enabled, or Google Gemini API key
- Google Cloud SDK (if using Vertex AI)

## Environment Setup

### 1. Install Dependencies

```bash
uv sync --all-extras
```

### 2. Install Additional Evaluation Dependencies

The evaluation requires the `rouge-score` package for response matching:

```bash
uv add rouge-score
```

### 3. Configure Environment Variables

Copy the environment template and configure your credentials:

```bash
cp .env.example .env
```

Edit the `.env` file with one of the following configurations:

**Option A: Google Cloud Vertex AI (Recommended)**
```env
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

**Option B: Google Gemini Developer API**
```env
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your-gemini-api-key
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

### 4. Authenticate (if using Vertex AI)

```bash
gcloud auth application-default login
gcloud services enable aiplatform.googleapis.com
```

## Running the Evaluation

Execute the evaluation tests using pytest:

```bash
uv run pytest eval -v
```

## Evaluation Test Cases

The evaluation consists of two main test scenarios:

### 1. Simple Test (`simple.test.json`)
Tests basic agent functionality with two interactions:
- **Greeting**: "hi," - Tests customer recognition and welcome response
- **Cart Inquiry**: "tell me what is in my cart?" - Tests tool usage and cart information retrieval

### 2. Full Conversation Test (`full_conversation.test.json`)
Tests complex multi-turn conversation handling including:
- Customer greeting and recognition
- Purchase history inquiries
- Product recommendations
- Cart modifications
- Service scheduling

## Evaluation Metrics

The evaluation uses two key metrics:

1. **Tool Trajectory Score**: Measures correctness of tool usage (expected threshold: 0.2)
2. **Response Match Score**: Measures response quality using ROUGE scoring (expected threshold: 0.2)

## Evaluation Results

For detailed evaluation results including test execution data, performance metrics, and behavioral verification, see:

📁 **[evaluation_results/](./evaluation_results/)** directory

**Latest Results:**
- [2025-07-24 Test Results](./evaluation_results/2025-07-24_test-results.md) - All tests PASSED with 98-second total execution time

## Troubleshooting

### Common Issues

1. **API Authentication Errors**
   - Verify Google Cloud credentials are properly configured
   - Ensure Vertex AI API is enabled in your project
   - Check API key validity for Gemini Developer API

2. **Missing Dependencies**
   - Ensure all extras are installed: `uv sync --all-extras`

3. **Evaluation Failures**
   - Check that test data files exist in `eval/eval_data/`
   - Verify environment variables are properly set
   - Ensure sufficient API quotas/credits

### Unit Tests (Optional)

While this guide focuses on evaluation tests, you can also run unit tests to verify individual components:

```bash
uv run pytest tests/unit
```

## Evaluation Output Schema

### Standard Metrics

The evaluation produces two key metrics defined in `test_config.json`:

#### Tool Trajectory Average Score
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures correctness of tool usage sequence and customer service workflow
- **Interpretation**:
  - 1.0 = Perfect tool usage with correct customer data retrieval
  - < 1.0 = Missing tool calls, incorrect tools used, or wrong customer data access
- **Threshold**: 0.2 (defined in `eval/eval_data/test_config.json`)

#### Response Match Score
- **Type**: Float (0.0 - 1.0) 
- **Description**: Measures response quality using ROUGE scoring against expected customer service responses
- **Interpretation**:
  - Higher values indicate better similarity to expected professional customer service responses
  - Accounts for natural variations in customer service communication
- **Threshold**: 0.2 (defined in `eval/eval_data/test_config.json`)

### Output Format Example

```
| Metric | Score | Threshold | Status |
|--------|-------|-----------|---------|
| Tool Trajectory Average Score | 1.0 | 0.2 | ✅ PASSED |
| Response Match Score | 0.48 | 0.2 | ✅ PASSED |
```

### Test Scenarios Evaluated

1. **Simple Test** (`simple.test.json`):
   - Basic customer recognition and greeting
   - Cart information retrieval using `access_cart_information` tool
   
2. **Full Conversation Test** (`full_conversation.test.json`):
   - Multi-turn customer service conversation
   - Purchase history queries, product recommendations, cart modifications

### Success Indicators
- ✅ **PASSED**: All metrics exceed threshold values (0.2)
- **Key Behaviors Verified**:
  - Correctly identifies returning customers
  - Successfully calls appropriate customer service tools
  - Accurately reports account information (cart contents, loyalty points, purchase history)
  - Maintains professional customer service tone throughout interactions

### Performance Characteristics
- **Total Evaluation Duration**: ~98 seconds (1 minute 38 seconds)
- **Simple Test**: ~3 seconds
- **Full Conversation Test**: ~95 seconds
- **Tool Integration**: Successful cart and customer data access
- **Conversational Flow**: Natural, helpful dialogue maintained

## Conclusion

The Customer Service Agent successfully passes both evaluation scenarios, demonstrating robust performance in customer interaction, tool usage, and response generation. The evaluation confirms the agent is ready for deployment in customer service scenarios.