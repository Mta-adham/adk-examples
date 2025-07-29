# RAG Agent - Previous Evaluation Results

## Overview
This file documents the expected evaluation results and setup requirements as outlined in the EVALUATION.md guide for the ADK RAG (Retrieval-Augmented Generation) agent.

## Expected Test Results (from EVALUATION.md)

### Test Environment Requirements
- **Access**: `evoml-mcp` Google Cloud project (required)
- **Expected Runtime**: 3-5 minutes
- **Timeout Setting**: 10 minutes (set in pytest)
- **Total Test Queries**: 22 queries about Alphabet 10-K report

### Test Configuration
From `eval/data/test_config.json`:
- **Tool Trajectory Threshold**: 0.09 (measures correct usage of `retrieve_rag_documentation` tool)
- **Response Match Threshold**: 0.4 (measures semantic similarity to reference answers)

### Expected Results Summary

#### Tool Trajectory Average Score
- **Threshold**: 0.09
- **Purpose**: Measures correct usage of `retrieve_rag_documentation` tool
- **Expected Status**: PASSED (score ≥ 0.09)

#### Response Match Score  
- **Threshold**: 0.4
- **Purpose**: Measures semantic similarity to reference answers
- **Expected Variability**: May vary due to generative nature of RAG systems
- **Expected Status**: Variable performance expected

## RAG Corpus Setup Requirements

### Document Source
- **Source URL**: https://abc.xyz/assets/77/51/9841ad5c4fbe85b4440c47a4df8d/goog-10-k-2024.pdf
- **Document**: Alphabet 2024 10-K financial report
- **Corpus Name**: 'Alphabet_10K_2024_corpus'

### Expected Setup Process
1. **Corpus Discovery**: Find or create corpus named 'Alphabet_10K_2024_corpus'
2. **Document Download**: Automatically download PDF from Alphabet investor relations
3. **Corpus Upload**: Upload document to RAG corpus
4. **Environment Update**: Automatically update `RAG_CORPUS` variable in `.env` file

### Expected Setup Output
```
Found existing corpus with display name 'Alphabet_10K_2024_corpus'
Updated RAG_CORPUS in /path/to/.env to projects/evoml-mcp/locations/us-central1/ragCorpora/[CORPUS_ID]
Downloading PDF from https://abc.xyz/assets/77/51/9841ad5c4fbe85b4440c47a4df8d/goog-10-k-2024.pdf...
PDF downloaded successfully to /tmp/[TEMP_PATH]/goog-10-k-2024.pdf
Uploading goog-10-k-2024.pdf to corpus...
Successfully uploaded goog-10-k-2024.pdf to corpus
Total files in corpus: [NUMBER]
```

## Technical Requirements

### Prerequisites
- Access to the `evoml-mcp` Google Cloud project (mandatory)
- `uv` package manager installed
- Git access to the repository

### Dependencies (Expected Installation)
- **Core**: `google-adk`, `google-cloud-aiplatform`, `llama-index`
- **Dev**: `pytest`, `pytest-asyncio`, `rouge-score`, `scikit-learn`
- **Installation Command**: `uv sync --dev`

### Authentication Requirements
```bash
gcloud auth application-default login --project=evoml-mcp
```

### Environment Configuration
Expected `.env` file contents:
```env
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=evoml-mcp
GOOGLE_CLOUD_LOCATION=us-central1
RAG_CORPUS=projects/PROJECT_NUMBER/locations/us-central1/ragCorpora/CORPUS_ID
STAGING_BUCKET=gs://evoml-mcp-staging
```

## Expected Evaluation Process

### Step-by-Step Workflow
1. **Environment Setup**: `uv sync --dev`
2. **Authentication**: `gcloud auth application-default login --project=evoml-mcp`
3. **Corpus Preparation**: `uv run python rag/shared_libraries/prepare_corpus_and_data.py`
4. **Evaluation Execution**: `uv run python -m pytest eval/test_eval.py -v -s`

### Test Data Structure
```
eval/
├── data/
│   ├── conversation.test.json    # 22 test queries and expected responses
│   └── test_config.json         # Evaluation thresholds
└── test_eval.py                 # Main evaluation script
```

## Expected Success Criteria

A successful evaluation should demonstrate:

1. ✅ **Tool trajectory score ≥ 0.09**
2. ✅ **Agent consistently uses RAG retrieval for information queries**
3. ✅ **Responses include proper citations from source documents**
4. ✅ **No authentication or permission errors**

## Expected Capabilities

### RAG Functionality
- **Document Retrieval**: Accurate retrieval from Alphabet 10-K corpus
- **Citation Management**: Proper attribution to source documents
- **Query Understanding**: Comprehension of complex financial and business questions
- **Response Generation**: Professional, contextually appropriate responses

### Technical Integration
- **Corpus Management**: Automatic setup and configuration
- **Authentication**: Seamless Google Cloud integration
- **Error Handling**: Graceful handling of retrieval and generation failures
- **Performance**: Reasonable response times for document-based queries

## Expected Query Types

The evaluation tests 22 different query categories:
- Financial performance metrics
- AI investment strategies
- Risk factor analysis
- Business operation details
- Regulatory compliance information
- Strategic initiatives and outlook

## Troubleshooting Expectations

### Common Expected Issues
1. **Authentication Errors**: Resolved by proper `gcloud auth application-default login --project=evoml-mcp`
2. **Missing RAG Corpus**: Resolved by running corpus preparation script
3. **Environment Variable Issues**: Resolved by verifying `.env` file configuration
4. **Dependency Issues**: Resolved by using `uv sync --dev` (not `--all-extras`)

### Performance Expectations
- **Response Time**: 3-5 minutes total evaluation time
- **Consistency**: Reliable performance across different query types
- **Accuracy**: High-quality responses with proper business context
- **Citation**: Consistent source attribution

## File Structure Reference
```
rag/
├── shared_libraries/
│   └── prepare_corpus_and_data.py  # RAG corpus setup script
├── agent.py                        # Main agent implementation
└── prompts.py                      # Agent prompts

.env                                # Environment configuration
pyproject.toml                      # Project dependencies
```

## Expected Post-Evaluation Assessment

After successful evaluation, expected outcomes:
1. Review of any failed response matches to understand semantic differences
2. Agent readiness confirmation for deployment using scripts in `deployment/`
3. Consideration of additional test scenarios if needed
4. Validation of consistent citation and retrieval practices

## Previous Assessment Conclusion

The RAG agent was expected to demonstrate strong capabilities in document-based question answering, with particular strength in:
- Accurate retrieval from structured financial documents
- Professional business communication
- Proper source attribution
- Comprehensive coverage of complex financial topics

The evaluation framework was designed to ensure consistent and successful evaluation across different AI agents and environments.