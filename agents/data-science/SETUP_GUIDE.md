# Data Science Agent Setup and Evaluation Guide

This guide documents the complete process for setting up and running the evaluation for the Data Science Multi-Agent system using the evoml-mcp GCP project.

## Prerequisites

- Python 3.12+
- uv (Python package manager)
- Google Cloud SDK (gcloud CLI)
- Access to evoml-mcp GCP project

## Step-by-Step Setup Process

### 1. Initial Environment Analysis

First, examine the project structure to understand the agent components:

```bash
# Check the current directory structure
ls -la /home/paul/Projects/artemis/agent-optimisation/fix/adk-agents/data-science/
```

Key files to review:
- `README.md` - Main documentation (uses Poetry, but we'll use uv)
- `EVALUATION.md` - Evaluation-specific instructions (uses uv)
- `pyproject.toml` - Project dependencies
- `.env.example` - Environment configuration template

### 2. Environment Configuration

Create the environment file:

```bash
# Copy the template
cp .env.example .env
```

Edit the `.env` file with the following evoml-mcp project configuration:

```env
# Choose Model Backend: 1 -> Vertex
GOOGLE_GENAI_USE_VERTEXAI=1

# ML Dev backend config (not used for Vertex)
GOOGLE_API_KEY=YOUR_VALUE_HERE

# Vertex backend config
GOOGLE_CLOUD_PROJECT=evoml-mcp
GOOGLE_CLOUD_LOCATION=us-central1

# SQLGen method
NL2SQL_METHOD="BASELINE" # BASELINE or CHASE

# Set up BigQuery Agent
BQ_COMPUTE_PROJECT_ID=evoml-mcp
BQ_DATA_PROJECT_ID=evoml-mcp
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

### 3. Install Dependencies

Use uv (not Poetry as mentioned in README.md) for dependency management:

```bash
# Install all dependencies including dev extras
uv sync --all-extras
```

This will:
- Create a virtual environment at `.venv`
- Install 132 packages including google-adk, google-cloud-aiplatform, pytest, etc.
- Build the local data-science package

### 4. Google Cloud Setup

Configure the GCP project and authentication:

```bash
# Set the active project
gcloud config set project evoml-mcp

# Authenticate with Application Default Credentials
gcloud auth application-default login

# Enable required Google Cloud services
gcloud services enable aiplatform.googleapis.com bigquery.googleapis.com
```

**Note**: You may see a warning about quota project mismatch - this is normal and doesn't affect functionality.

### 5. BigQuery Data Setup

Load the required test data into BigQuery:

```bash
# Run the data setup script
uv run python data_science/utils/create_bq_table.py
```

This creates:
- Dataset: `evoml-mcp.forecasting_sticker_sales`
- Table: `train` (229,680 rows of historical sticker sales data)
- Table: `test` (440 rows of recent sticker sales data)

Both tables have the schema:
- `id` (INTEGER): Unique identifier
- `date` (DATE): Sale date
- `country` (STRING): Country where sale occurred
- `store` (STRING): Store name
- `product` (STRING): Product name (various sticker types)
- `num_sold` (INTEGER): Number of units sold

### 6. Run the Evaluation

Execute the evaluation tests:

```bash
# Run the evaluation with verbose output
uv run pytest eval -v
```

## Expected Evaluation Process

The evaluation will:

1. **Create Code Interpreter Extension**: If not already existing, a Vertex AI Code Interpreter extension will be created automatically (takes ~20 seconds)

2. **Load Test Data**: The evaluation uses `eval/eval_data/simple.test.json` which tests:
   - "what data do you have?" - Tests schema knowledge
   - "what countries are in test?" - Tests database querying

3. **Multi-Agent Execution**: The system will:
   - Route queries to appropriate sub-agents (db_agent, ds_agent, bqml_agent)
   - Execute BigQuery queries
   - Generate natural language responses

4. **Validation**: Tests both:
   - Tool trajectory score (correct tool usage) - threshold: 0.5
   - Response match score (response quality using ROUGE) - threshold: 0.1

## Known Issues and Solutions

### Minor Warning
You may see this warning (safe to ignore):
```
Contents of simple.test.json appear to be in older format. To avoid this warning, please update your test files to contain data in EvalSet schema.
```

This doesn't affect functionality - the system uses backward compatibility.

### Troubleshooting Common Issues

1. **BigQuery Dataset Not Found**
   - Ensure `uv run python data_science/utils/create_bq_table.py` completed successfully
   - Verify BigQuery API is enabled
   - Check dataset exists in Google Cloud Console

2. **Authentication Errors**
   - Re-run `gcloud auth application-default login`
   - Verify project ID matches in `.env` file
   - Ensure Vertex AI API is enabled

3. **Dependency Issues**
   - Use `uv sync --all-extras` (not `poetry install`)
   - Ensure Python 3.12+ is available

## Expected Success Output

A successful evaluation will show:
- Code Interpreter extension creation (if first run)
- BigQuery queries executing successfully
- Agent responses with proper schema knowledge
- Test passing with PASSED status

## Agent Architecture Verified

The evaluation confirms the multi-agent system works correctly:

- **Root Agent**: Intent classification and routing
- **Database Agent**: SQL query generation and BigQuery execution
- **Analytics Agent**: Python-based data analysis
- **BQML Agent**: BigQuery ML operations

## Performance Notes

- **Execution Time**: ~1-2 minutes for simple evaluation
- **BigQuery Costs**: Minimal query costs for test dataset
- **Vertex AI Usage**: Uses Gemini 2.5 Flash models for efficiency
- **One-time Setup**: Code Interpreter extension creation happens once

## File Structure Summary

```
data-science/
├── .env                           # Environment configuration
├── .env.example                   # Template for environment vars
├── README.md                      # Main documentation (uses Poetry)
├── EVALUATION.md                  # Evaluation guide (uses uv - follow this)
├── pyproject.toml                 # Project dependencies
├── data_science/                  # Main agent code
│   ├── agent.py                   # Root agent
│   ├── sub_agents/                # Specialized agents
│   └── utils/                     # Utilities and data
├── eval/                          # Evaluation tests
│   └── eval_data/                 # Test scenarios
└── evaluation_results/            # Previous evaluation results
```

## Key Differences from README.md

- **Use uv instead of Poetry**: The EVALUATION.md correctly specifies uv
- **Follow EVALUATION.md**: More accurate than README.md for setup process
- **Environment Variables**: Use evoml-mcp project configuration
- **Testing Command**: `uv run pytest eval -v` (not `poetry run pytest eval`)

This setup process ensures the data science agent is fully functional and ready for use with comprehensive BigQuery integration and multi-agent orchestration.