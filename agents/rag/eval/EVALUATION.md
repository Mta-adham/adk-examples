# RAG Agent Evaluation Guide for AI Agents

This document provides step-by-step instructions for AI agents to set up and run the evaluation for the ADK RAG (Retrieval-Augmented Generation) agent.

## Prerequisites

Before starting, ensure you have:
- Access to a Google Cloud project with Vertex AI and RAG APIs enabled
- `uv` package manager installed
- Git access to the repository

**Note**: This guide is configured for the `evoml-mcp` project. Update project references as needed for your environment.

## Step-by-Step Evaluation Process

### 1. Environment Setup

First, install the dependencies using uv with the development flag as specified in SETUP_AND_EVALUATION.md:

```bash
uv sync --dev
```

This installs both production and development dependencies including:
- Core: `google-adk`, `google-cloud-aiplatform`, `llama-index`
- Dev: `pytest`, `pytest-asyncio`, `rouge-score`, `scikit-learn`

### 2. Google Cloud Authentication

Authenticate with Google Cloud using the evoml-mcp project:

```bash
gcloud auth application-default login --project=evoml-mcp
```

This will open a browser window for authentication. Complete the OAuth flow to save credentials.

### 3. Environment Configuration

Create/update the `.env` file with the correct project settings:

```env
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=evoml-mcp
GOOGLE_CLOUD_LOCATION=us-central1
RAG_CORPUS=projects/PROJECT_NUMBER/locations/us-central1/ragCorpora/CORPUS_ID
STAGING_BUCKET=gs://evoml-mcp-staging
```

**Note:** The `RAG_CORPUS` value will be automatically updated by the corpus setup script.

### 4. RAG Corpus Setup

Run the corpus preparation script to set up the Alphabet 10-K document:

```bash
uv run python rag/shared_libraries/prepare_corpus_and_data.py
```

This script will:
- Find or create a corpus named 'Alphabet_10K_2024_corpus'
- Download the Alphabet 2024 10-K PDF from https://abc.xyz/assets/77/51/9841ad5c4fbe85b4440c47a4df8d/goog-10-k-2024.pdf
- Upload the document to the RAG corpus
- Automatically update the `RAG_CORPUS` variable in your `.env` file

**Expected Output:**
```
Found existing corpus with display name 'Alphabet_10K_2024_corpus'
Updated RAG_CORPUS in /path/to/.env to projects/evoml-mcp/locations/us-central1/ragCorpora/[CORPUS_ID]
Downloading PDF from https://abc.xyz/assets/77/51/9841ad5c4fbe85b4440c47a4df8d/goog-10-k-2024.pdf...
PDF downloaded successfully to /tmp/[TEMP_PATH]/goog-10-k-2024.pdf
Uploading goog-10-k-2024.pdf to corpus...
Successfully uploaded goog-10-k-2024.pdf to corpus
Total files in corpus: [NUMBER]
```

### 5. Run the Evaluation

Execute the evaluation using pytest:

```bash
uv run pytest eval -v -s
```

**Important:** Use `uv run` to ensure the virtual environment is used correctly.

### 6. Interpret Results

The evaluation tests 22 queries and measures two key metrics:

#### Tool Trajectory Average Score
- **Threshold:** 0.09
- **Purpose:** Measures correct usage of `retrieve_rag_documentation` tool
- **Expected:** PASSED (score ≥ 0.09)

#### Response Match Score  
- **Threshold:** 0.4
- **Purpose:** Measures semantic similarity to reference answers
- **Note:** May vary due to generative nature of RAG systems

### Expected Evaluation Runtime
- **Duration:** 3-5 minutes
- **Timeout:** 10 minutes (set in pytest)

## Troubleshooting Common Issues

### Authentication Errors
```bash
google.genai.errors.ClientError: 403 PERMISSION_DENIED
```
**Solution:** Ensure you've run `gcloud auth application-default login --project=evoml-mcp`

### Missing RAG Corpus
```bash
Error: RAG corpus not found
```
**Solution:** Run `uv run python rag/shared_libraries/prepare_corpus_and_data.py`

### Environment Variable Issues
**Solution:** Verify `.env` file has correct values:
- `GOOGLE_CLOUD_PROJECT=evoml-mcp`
- `GOOGLE_CLOUD_LOCATION=us-central1`
- `RAG_CORPUS` should be auto-populated by the setup script

### Dependency Issues
**Solution:** Use `uv sync --dev` to install development dependencies

## File Structure Reference

```
eval/
├── data/
│   ├── conversation.test.json    # 22 test queries and expected responses
│   └── test_config.json         # Evaluation thresholds
└── test_eval.py                 # Main evaluation script

rag/
├── shared_libraries/
│   └── prepare_corpus_and_data.py  # RAG corpus setup script
├── agent.py                     # Main agent implementation
└── prompts.py                   # Agent prompts

.env                             # Environment configuration
pyproject.toml                   # Project dependencies
```

## Success Criteria

A successful evaluation should show:
1. ✅ Tool trajectory score ≥ 0.09
2. Agent consistently uses RAG retrieval for information queries
3. Responses include proper citations from source documents
4. No authentication or permission errors

## Post-Evaluation

After successful evaluation:
1. Review any failed response matches to understand semantic differences
2. The agent is ready for deployment using scripts in `deployment/`
3. Consider running additional test scenarios if needed

## Evaluation Output Schema

### Standard Metrics

The evaluation tests 22 queries and measures two key metrics from `eval/data/test_config.json`:

#### Tool Trajectory Average Score
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures correct usage of `retrieve_rag_documentation` tool for information retrieval
- **Interpretation**:
  - 0.09+ = Acceptable RAG tool usage for document retrieval queries
  - < 0.09 = Insufficient tool usage or incorrect document retrieval
- **Threshold**: 0.09 (defined in `eval/data/test_config.json`)

#### Response Match Score
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures semantic similarity to reference answers using ROUGE scoring
- **Interpretation**:
  - 0.4+ = High-quality responses with proper document-grounded information
  - 0.3-0.4 = Acceptable responses with some variations due to generative nature
  - < 0.3 = Insufficient response quality or missing source information
- **Threshold**: 0.4 (defined in `eval/data/test_config.json`)

### RAG-Specific Evaluation

The evaluation specifically tests:
- **Document Retrieval**: Proper use of `retrieve_rag_documentation` tool for information queries
- **Source Citations**: Inclusion of proper citations from source documents (Alphabet 10-K 2024)
- **Information Accuracy**: Grounding of responses in retrieved document content
- **Query Handling**: Appropriate responses to 22 diverse test queries about financial information

### Output Format Example

```
✅ Tool trajectory score ≥ 0.09
✅ Agent consistently uses RAG retrieval for information queries  
✅ Responses include proper citations from source documents
✅ No authentication or permission errors
```

### Test Configuration

- **Test Data**: `eval/data/conversation.test.json` (22 test queries)
- **Expected Runtime**: 3-5 minutes
- **Timeout**: 10 minutes (set in pytest)
- **RAG Corpus**: Alphabet 10-K 2024 document from https://abc.xyz/assets/77/51/9841ad5c4fbe85b4440c47a4df8d/goog-10-k-2024.pdf

### Success Indicators

A successful evaluation should demonstrate:
1. ✅ **Tool Trajectory Score** ≥ 0.09 (consistent RAG retrieval usage)
2. ✅ **Response Quality**: Agent responses grounded in retrieved document content
3. ✅ **Source Citations**: Proper attribution to Alphabet 10-K source material
4. ✅ **Document Integration**: Effective integration of RAG corpus information

### Evaluation Variations

**Response Match Score Variability**:
- May vary due to generative nature of RAG systems
- Natural language variations in document-based responses
- Different but equivalent ways to present financial information
- Acceptable as long as information remains accurate and well-sourced

### Performance Characteristics
- **Evaluation Duration**: 3-5 minutes for 22 test queries
- **Document Processing**: Automatic RAG corpus setup with Alphabet 10-K PDF
- **Tool Usage**: Consistent retrieval tool usage across information queries
- **Citation Quality**: Proper source attribution maintained throughout responses

---

*This guide ensures consistent and successful evaluation of the RAG agent across different AI agents and environments.*