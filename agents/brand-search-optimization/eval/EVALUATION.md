# Brand Search Optimization Agent Evaluation Guide

This guide provides instructions for setting up and running the evaluation tests for the Brand Search Optimization Agent.

## Overview

The Brand Search Optimization Agent is an AI-powered assistant built using Google's Agent Development Kit (ADK). It is designed to enhance product titles for retail brand search by retrieving top keywords, performing searches, and analyzing top results to provide suggestions for enriching product titles.

## Prerequisites

- Python 3.11+
- uv (for dependency management)
- Google Cloud Project with Vertex AI enabled, or Google Gemini API key
- Google Cloud SDK (if using Vertex AI)
- BigQuery access for product data

## Environment Setup

### 1. Install Dependencies

```bash
uv sync --all-extras
```

### 2. Configure Environment Variables

Copy the environment template and configure your credentials:

```bash
cp .env.example .env
```

Edit the `.env` file with the following configuration:

**Google Cloud Vertex AI Configuration**
```env
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=evoml-mcp
GOOGLE_CLOUD_LOCATION=us-central1
MODEL="gemini-2.5-flash"

DATASET_ID="products_data_agent"
TABLE_ID="shoe_items"

# IMPORTANT: Setting this flag to 1 will disable web driver
DISABLE_WEB_DRIVER=1

# Staging bucket name for ADK agent deployment
STAGING_BUCKET=evoml-mcp
```

### 4. Set Up BigQuery Data

The agent requires sample product data in BigQuery. Run the data population script:

```bash
uv run python -m deployment.bq_populate_data
```

This will:
- Create the dataset `products_data_agent` 
- Create the table `shoe_items`
- Insert sample shoe product data

## Running Evaluations

### Method 1: Using pytest (Recommended)

Run the evaluation tests using pytest:

```bash
uv run pytest eval -v
```

### Method 2: Using ADK CLI

Run the full ADK evaluation:

```bash
uv run adk eval brand_search_optimization eval/data/eval_data1.evalset.json --config_file_path eval/data/test_config.json
```

### Method 3: Using Shell Script

Run the provided evaluation script:

```bash
bash deployment/eval.sh
```

## Evaluation Results

The agent can be evaluated using pytest, ADK CLI, or shell scripts as described above. See the evaluation configuration and troubleshooting sections for details on running tests and interpreting results.

## Troubleshooting

### Common Issues

1. **Missing Dependencies**:
   ```bash
   uv sync --all-extras
   ```

2. **BigQuery Permissions**:
   - Ensure your GCP account has BigQuery admin permissions
   - Check the `customization.md` file for detailed permission instructions

3. **Web Driver Warnings**:
   - These are non-fatal and don't prevent evaluation completion
   - Ensure `DISABLE_WEB_DRIVER=1` is set in your `.env` file

4. **ADK CLI Not Found**:
   - Ensure you're using `uv run adk` instead of just `adk`
   - Reinstall with all extras: `uv sync --all-extras`

## Evaluation Output Schema

### Standard Metrics

The evaluation produces two primary metrics in a standardized format:

#### Tool Trajectory Average Score
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures correctness of tool usage sequence and agent workflow
- **Interpretation**: 
  - 1.0 = Perfect tool usage with correct sequence and parameters
  - < 1.0 = Missing tool calls, incorrect tools used, or wrong parameters
- **Threshold**: Not specified in current configuration

#### Response Match Score  
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures semantic similarity between agent response and expected output using ROUGE scoring
- **Interpretation**:
  - Higher values indicate better similarity to expected responses
  - Accounts for paraphrasing and equivalent explanations
- **Threshold**: Not specified in current configuration

### Output Format Example

```
| Metric | Score | Threshold | Status |
|--------|-------|-----------|---------|
| Tool Trajectory Average Score | 1.0 | N/A | ✅ SUCCESS |
| Response Match Score | 0.85 | N/A | ✅ SUCCESS |
```

### Success Indicators
- ✅ **PASSED**: Metric meets or exceeds threshold
- ⚠️ **WARNING**: Partial success with known issues  
- ❌ **FAILED**: Metric below threshold or execution error

### Execution Metadata
- **Duration**: Execution time in seconds (float)
- **Test Runs**: Number of evaluation iterations (typically 1-5)
- **Environment**: Configuration details (uv setup, dependencies, APIs)

## Next Steps

1. Update agent code for ADK API compatibility
2. Resolve web driver configuration issues  
3. Implement more comprehensive evaluation test cases
4. Consider performance benchmarking with realistic product data