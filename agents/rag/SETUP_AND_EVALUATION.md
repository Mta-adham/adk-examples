# RAG Agent Setup and Evaluation Guide

This document describes the process for setting up the environment and running the evaluation for the ADK RAG (Retrieval-Augmented Generation) agent.

## Overview

The RAG agent is designed to answer questions about Alphabet's 10-K financial report using Vertex AI RAG Engine. The evaluation tests the agent's ability to retrieve relevant information and provide accurate responses to complex financial and business questions.

## Environment Setup

### Prerequisites

- Python 3.11+ (automatically handled by `uv`)
- `uv` package manager (version 0.6.14 or later)
- Google Cloud Project with Vertex AI enabled
- Access to a configured RAG corpus in Vertex AI

### Setup Steps

1. **Install Dependencies**
   ```bash
   uv sync --dev
   ```
   This installs both production and development dependencies, including:
   - Core dependencies: `google-adk`, `google-cloud-aiplatform`, `llama-index`
   - Dev dependencies: `pytest`, `pytest-asyncio`, `rouge-score`, `scikit-learn`

2. **Environment Configuration**
   The `.env` file must be configured with:
   ```env
   GOOGLE_GENAI_USE_VERTEXAI=1
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   RAG_CORPUS=projects/PROJECT_NUMBER/locations/us-central1/ragCorpora/CORPUS_ID
   STAGING_BUCKET=gs://your-staging-bucket
   ```

3. **Virtual Environment**
   `uv` automatically creates and manages a Python 3.13.3 virtual environment in `.venv/`

## Running the Evaluation

### Command
```bash
.venv/bin/python -m pytest eval/test_eval.py -v -s
```

### Evaluation Process

The evaluation tests the agent against 22 queries covering various aspects of Alphabet's 10-K report, including:
- Financial performance metrics
- AI investment strategies
- Regulatory challenges
- Accounting policies
- Business segment analysis
- Risk factors

### Expected Runtime
- **Duration**: 3-5 minutes
- **Timeout**: Set to 10 minutes to accommodate API calls and document retrieval

## Evaluation Metrics

The evaluation uses two primary metrics:

### 1. Tool Trajectory Average Score
- **Threshold**: 0.09
- **Purpose**: Measures whether the agent correctly uses the `retrieve_rag_documentation` tool
- **Result**: ✅ **PASSED** (0.091 vs 0.09 threshold)

### 2. Response Match Score
- **Threshold**: 0.4
- **Purpose**: Measures semantic similarity between agent responses and reference answers
- **Result**: ❌ **FAILED** (0.313 vs 0.4 threshold)

## Expected Outcomes

### Normal Results
- **Tool Usage**: The agent should consistently call the RAG retrieval tool for information-seeking queries
- **Response Quality**: Responses should be factually accurate and well-cited, even if they don't exactly match reference text
- **Citation Format**: All responses should include proper citations from the source document

### Common Patterns
1. **Greeting Queries**: Simple acknowledgments without tool calls
2. **Information Queries**: Proper tool usage with relevant search terms
3. **Complex Analysis**: Multi-faceted responses drawing from various document sections

## Troubleshooting

### Common Issues
1. **Timeout Errors**: Increase pytest timeout if evaluation takes longer than expected
2. **Authentication**: Ensure Google Cloud credentials are properly configured
3. **RAG Corpus Access**: Verify the corpus ID and project permissions

### Performance Considerations
- Response matching scores may vary due to the generative nature of RAG systems
- Tool trajectory scores should consistently meet or exceed the threshold
- Evaluation duration depends on network latency and model response times

## File Structure
```
eval/
├── data/
│   ├── conversation.test.json    # Test queries and expected responses
│   └── test_config.json         # Evaluation thresholds
└── test_eval.py                 # Main evaluation script
```

## Next Steps

After successful evaluation:
1. Review failed response matches to understand semantic differences
2. Consider adjusting response generation prompts if needed
3. Deploy the agent using the deployment scripts in `deployment/`
4. Monitor performance in production environments

---

*This evaluation framework ensures the RAG agent maintains quality standards while providing accurate, well-sourced responses to complex financial document queries.*