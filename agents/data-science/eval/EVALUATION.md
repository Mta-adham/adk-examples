# Data Science Agent Evaluation Guide

This guide provides instructions for setting up and running the evaluation tests for the Data Science and Data Analytics Multi-Agent System.

## Overview

The Data Science Agent is an AI-powered assistant built using Google's Agent Development Kit (ADK). It provides comprehensive data science capabilities including SQL database querying, Python data analysis, and BigQuery ML operations through specialized sub-agents. The system is designed to handle complex data science workflows from data exploration to advanced analytics.

## Prerequisites

- Python 3.12+
- uv (for dependency management)
- Google Cloud Project with BigQuery and Vertex AI enabled
- Google Cloud SDK (gcloud CLI)
- BigQuery dataset with test data

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

Edit the `.env` file with your configuration:

```env
# Choose Model Backend: 0 -> ML Dev, 1 -> Vertex
GOOGLE_GENAI_USE_VERTEXAI=1

# ML Dev backend config. Fill if using Ml Dev backend.
GOOGLE_API_KEY=YOUR_VALUE_HERE

# Vertex backend config
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# SQLGen method
NL2SQL_METHOD="BASELINE" # BASELINE or CHASE

# Set up BigQuery Agent
BQ_COMPUTE_PROJECT_ID=your-project-id
BQ_DATA_PROJECT_ID=your-project-id
BQ_DATASET_ID='forecasting_sticker_sales'

# Set up RAG Corpus for BQML Agent
BQML_RAG_CORPUS_NAME='' # Leave this empty as it will be populated automatically

# Set up Code Interpreter, if it exists. Else leave empty
CODE_INTERPRETER_EXTENSION_NAME='' # Either '' or 'projects/{GOOGLE_CLOUD_PROJECT}/locations/us-central1/extensions/{EXTENSION_ID}'

# Models used in Agents
ROOT_AGENT_MODEL='gemini-2.5-flash'
ANALYTICS_AGENT_MODEL='gemini-2.5-flash'
BIGQUERY_AGENT_MODEL='gemini-2.5-flash'
BASELINE_NL2SQL_MODEL='gemini-2.5-flash'
CHASE_NL2SQL_MODEL='gemini-2.5-flash'
BQML_AGENT_MODEL='gemini-2.5-flash'
```

### 3. Authenticate with Google Cloud

```bash
gcloud auth application-default login
gcloud services enable aiplatform.googleapis.com
gcloud services enable bigquery.googleapis.com
```

### 4. Set Up Test Data in BigQuery

The agent requires specific BigQuery tables for evaluation. Run the provided setup script:

```bash
uv run python data_science/utils/create_bq_table.py
```

This will create:
- Dataset: `forecasting_sticker_sales`
- Table: `train` (229,680 rows of historical sticker sales data)
- Table: `test` (440 rows of recent sticker sales data)

Both tables contain the following schema:
- `id` (INTEGER): Unique identifier
- `date` (DATE): Sale date
- `country` (STRING): Country where sale occurred
- `store` (STRING): Store name
- `product` (STRING): Product name (various sticker types)
- `num_sold` (INTEGER): Number of units sold

## Running the Evaluation

Execute the evaluation tests using pytest:

```bash
uv run pytest eval -v
```

## Evaluation Test Cases

The evaluation consists of a simple test scenario that validates core agent functionality:

### Simple Test (`simple.test.json`)
Tests basic agent functionality with two interactions:

1. **Data Exploration**: "what data do you have?" - Tests agent's ability to describe available datasets and schema
2. **SQL Query**: "what countries are in test?" - Tests database querying capabilities through BigQuery integration

## Evaluation Metrics

The evaluation uses two key metrics:

1. **Tool Trajectory Score**: Measures correctness of tool usage and agent routing (threshold: 0.5)
2. **Response Match Score**: Measures response quality using ROUGE scoring (threshold: 0.1)

## Agent Architecture

The Data Science Agent operates as a multi-agent system with the following components:

### Root Agent (`data_science`)
- **Purpose**: Intent classification and agent routing
- **Capabilities**: Understands user queries and routes to appropriate sub-agents
- **Tools**: `call_db_agent`, `call_ds_agent`, `transfer_to_agent`

### Database Agent (`bigquery`)
- **Purpose**: SQL query generation and execution
- **Capabilities**: Natural language to SQL conversion, query optimization
- **Backend**: BigQuery integration with BASELINE/CHASE SQL generation methods

### Analytics Agent (`analytics`)
- **Purpose**: Python-based data analysis and visualization
- **Capabilities**: Statistical analysis, data processing, chart generation

### BQML Agent (`bqml`)
- **Purpose**: BigQuery ML operations
- **Capabilities**: Model training, inference, ML pipeline management

## Test Results Analysis

### Expected Behavior Verification

The evaluation confirms the agent demonstrates:

1. **Schema Knowledge**: Correctly identifies and describes available BigQuery tables without unnecessary tool calls
2. **Tool Integration**: Properly routes database queries to the BigQuery sub-agent
3. **SQL Generation**: Successfully generates and executes SQL queries for data exploration
4. **Response Formatting**: Provides well-structured, informative responses with proper explanations
5. **Multi-Agent Coordination**: Effectively coordinates between root agent and specialized sub-agents

### Key Success Indicators

- ✅ **Direct Schema Responses**: Agent answers schema questions without calling sub-agents
- ✅ **Accurate SQL Routing**: Database queries properly routed to `call_db_agent`
- ✅ **Correct Results**: SQL queries return accurate results from BigQuery
- ✅ **Clear Explanations**: Agent provides step-by-step explanations of data retrieval process

## Troubleshooting

### Common Issues

1. **BigQuery Dataset Not Found**
   - Run the data setup script: `uv run python data_science/utils/create_bq_table.py`
   - Verify BigQuery API is enabled: `gcloud services enable bigquery.googleapis.com`
   - Check dataset exists in Google Cloud Console

2. **Authentication Errors**
   - Verify Google Cloud credentials: `gcloud auth application-default login`
   - Ensure Vertex AI API is enabled: `gcloud services enable aiplatform.googleapis.com`
   - Check project ID matches in `.env` file

3. **Evaluation Threshold Failures**
   - Review `eval/eval_data/test_config.json` for threshold settings
   - Tool trajectory threshold: 0.5 (measures correct tool usage)
   - Response match threshold: 0.1 (measures response quality)

4. **Code Interpreter Extension Errors**
   - Extension is created automatically during first run
   - Check Google Cloud Console for extension status
   - Ensure sufficient Vertex AI quotas

### Performance Considerations

- **Execution Time**: ~1-2 minutes for simple evaluation
- **BigQuery Costs**: Minimal query costs for test dataset
- **Vertex AI Usage**: Uses Gemini 2.5 Flash models for efficiency
- **Extension Creation**: One-time setup creates code interpreter extension

## Extending the Evaluation

To add more comprehensive test cases:

1. **Create Additional Test Files**: Add new `.test.json` files in `eval/eval_data/`
2. **Update Test Runner**: Modify `eval/test_eval.py` to include new test files
3. **Adjust Thresholds**: Update `eval/eval_data/test_config.json` based on expected performance
4. **Add Complex Scenarios**: Include multi-step workflows, visualization requests, or ML operations

## Evaluation Output Schema

### Standard Metrics

The evaluation uses two key metrics defined in `eval/eval_data/test_config.json`:

#### Tool Trajectory Average Score
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures correctness of tool usage and agent routing across the multi-agent system
- **Interpretation**:
  - 1.0 = Perfect routing between root, database, analytics, and BQML agents
  - 0.5+ = Acceptable agent coordination and tool selection
  - < 0.5 = Poor agent routing or missing tool calls  
- **Threshold**: 0.5 (defined in `eval/eval_data/test_config.json`)

#### Response Match Score
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures response quality using ROUGE scoring for data science explanations
- **Interpretation**:
  - Higher values indicate better similarity to expected data science responses
  - Accounts for technical explanations and data analysis variations
  - Lower threshold due to variability in data science explanations
- **Threshold**: 0.1 (defined in `eval/eval_data/test_config.json`)

### Multi-Agent Architecture Evaluation

The evaluation specifically tests:
- **Root Agent** (`data_science`): Intent classification and agent routing
- **Database Agent** (`bigquery`): SQL query generation and execution  
- **Analytics Agent** (`analytics`): Python-based data analysis
- **BQML Agent** (`bqml`): BigQuery ML operations

### Output Format Example

```
✅ Direct Schema Responses: Agent answers schema questions without calling sub-agents
✅ Accurate SQL Routing: Database queries properly routed to call_db_agent
✅ Correct Results: SQL queries return accurate results from BigQuery
✅ Clear Explanations: Agent provides step-by-step explanations of data retrieval process
```

### Test Scenarios Evaluated

**Simple Test** (`simple.test.json`):
1. **Data Exploration**: "what data do you have?" - Tests schema knowledge
2. **SQL Query**: "what countries are in test?" - Tests BigQuery integration

### Success Indicators
- ✅ **Schema Knowledge**: Correctly identifies available BigQuery tables without unnecessary tool calls
- ✅ **Tool Integration**: Properly routes database queries to the BigQuery sub-agent  
- ✅ **SQL Generation**: Successfully generates and executes SQL queries for data exploration
- ✅ **Response Formatting**: Provides well-structured, informative responses with proper explanations
- ✅ **Multi-Agent Coordination**: Effectively coordinates between root agent and specialized sub-agents

### Performance Characteristics
- **Execution Time**: ~1-2 minutes for simple evaluation
- **BigQuery Costs**: Minimal query costs for test dataset (229,680 + 440 rows)
- **Vertex AI Usage**: Uses Gemini 2.5 Flash models for efficiency
- **Extension Creation**: One-time setup creates code interpreter extension automatically

## Conclusion

The Data Science Agent evaluation demonstrates robust performance in data exploration and database querying scenarios. The multi-agent architecture effectively handles intent classification, tool routing, and specialized task execution. The evaluation confirms the agent is ready for deployment in data science and analytics workflows requiring BigQuery integration and intelligent query processing.