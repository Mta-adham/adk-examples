# ADK Agents - Requirements and Setup Guide

This directory contains 11 agents built with Google's Agent Development Kit (ADK). Each agent demonstrates different AI capabilities and integrations with Google Cloud services.

## Agent Evaluations

All agents in this directory include evaluation suites. Each agent has:

- **Evaluation Guide**: Located at `agents/{agent-name}/eval/EVALUATION.md`
- **Test Cases**: Detailed scenarios and expected behaviors
- **Performance Benchmarks**: Metrics and success criteria
- **Expected Outputs**: Sample results and response formats

### Running Evaluations

All evaluations can be executed using:
```bash
uv run pytest eval
```

### Google Cloud Setup Required

A Google Cloud account is required to run evaluations. Configure your environment using the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) by following our setup guide: `@adk-agents/docs/GOOGLE_CLOUD_SETUP.md`

Both the evaluation guides and Google Cloud setup guide can be followed by AI agents such as Claude Code for automated setup and testing.

## Quick Start Requirements

### Core Prerequisites
- **Python**: ≥3.9 (most agents require ≥3.11)
- **Google Cloud Project** with billing enabled
- **Google ADK**: ≥1.0.0 (installed automatically with each agent)

### Authentication Setup
```bash
# Install Google Cloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate for local development
gcloud auth application-default login

# Set quota project (recommended)
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
```

### Environment Configuration
Each agent requires a `.env` file with these core variables:
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=1
```

## Agents Overview

| Agent | Purpose | Python | Special Requirements |
|-------|---------|--------|---------------------|
| **Academic Research** | Research paper exploration with Google Search | ≥3.9 | None |
| **Brand Search Optimization** | Web scraping for retail search optimization | ≥3.11 | Chrome WebDriver, BigQuery |
| **Customer Service** | AI-powered customer support system | ≥3.11 | None |
| **Data Science** | BigQuery analytics with ML capabilities | ≥3.12 | BigQuery datasets, RAG corpus |
| **Financial Advisor** | Multi-agent financial analysis system | ≥3.9 | None |
| **Image Scoring** | Automated image generation and evaluation | ≥3.11 | Vertex AI Imagen access |
| **LLM Auditor** | Fact-checking layer for LLM responses | ≥3.10 | None |
| **Marketing Agency** | Creative agency assistant for launches | ≥3.11 | None |
| **Personalized Shopping** | E-commerce product recommendations | ≥3.11, <3.13 | 5.1GB dataset download |
| **RAG** | Document retrieval with Vertex AI RAG | ≥3.11 | RAG corpus setup |
| **Travel Concierge** | Multi-agent travel management system | ≥3.11 | Google Places API, Node.js |

## Google Cloud Services Required

### Essential Services (Enable in Console)
```bash
# Core AI Platform services
gcloud services enable aiplatform.googleapis.com
gcloud services enable generativelanguage.googleapis.com

# Service-specific (as needed)
gcloud services enable bigquery.googleapis.com           # Data Science, Brand Search
gcloud services enable storage.googleapis.com            # Image Scoring, Deployment
gcloud services enable places.googleapis.com             # Travel Concierge
```

### IAM Permissions for Deployment
When deploying agents to Vertex AI Agent Engine, the service account needs additional permissions:
```bash
# Get your project number
PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")

# Grant AI Platform permissions
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"
```

## Running an Agent

### 1. Choose and Navigate to Agent
```bash
cd academic-research  # or any agent directory
```

### 2. Install Dependencies
```bash
pip install -e .
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your project details
```

### 4. Run Local Tests
```bash
python -m pytest tests/
```

### 5. Test Agent Locally
```bash
python -c "
from academic_research.agent import agent
result = agent.invoke({'input': 'Tell me about transformer architecture'})
print(result)
"
```

## Advanced Setup Requirements

### Brand Search Optimization
- **BigQuery Setup**: Create dataset and populate with product data
- **Chrome WebDriver**: Install for web scraping functionality
```bash
# Install Chrome WebDriver
sudo apt-get install chromium-chromedriver  # Ubuntu/Debian
```

### Data Science Agent
- **BigQuery Datasets**: Create analytics tables
- **RAG Corpus**: Set up Vertex AI RAG with ML documentation
```bash
python data_science/utils/create_bq_table.py
python data_science/utils/reference_guide_RAG.py
```

### Image Scoring Agent
- **Vertex AI Imagen**: Request access to Imagen 3.0
- **Cloud Storage**: Create bucket for image artifacts

### Personalized Shopping Agent
- **Large Dataset**: Downloads 5.1GB of product data automatically
- **Search Index**: PySerini-based product search engine setup

### RAG Agent
- **Document Corpus**: Upload and process documents
```bash
bash deployment/grant_permissions.sh
python rag/shared_libraries/prepare_corpus_and_data.py
```

### Travel Concierge Agent
- **Google Maps Platform**: Enable Places API
- **Node.js/NPX**: For MCP (Model Context Protocol) integration

## Deployment to Production

### 1. Create Cloud Storage Bucket
```bash
gsutil mb gs://your-agent-bucket
```

### 2. Deploy Agent
```bash
cd your-agent-directory
python deployment/deploy.py --create
```

### 3. Test Deployed Agent
```bash
python deployment/test_deployment.py
```

## Authentication Alternatives

### Option 1: Vertex AI (Recommended)
- Uses Application Default Credentials
- Full Google Cloud integration
- Required for most advanced features

### Option 2: Google AI Studio API Key
- Simpler setup for basic agents
- Limited functionality
- Set `GOOGLE_GENAI_USE_VERTEXAI=0` and `GOOGLE_API_KEY=your-key`

## Troubleshooting

### Common Issues

**Permission Denied**: Run `gcloud auth application-default login`

**Quota Exceeded**: Set quota project with `gcloud auth application-default set-quota-project`

**Missing APIs**: Enable required services in Google Cloud Console

**Import Errors**: Install agent with `pip install -e .` from agent directory

### Getting Help
- Check individual agent README files for specific setup instructions
- Review `EVALUATION.md` files for expected behavior and test cases
- Examine `deployment/` directories for cloud deployment examples

## Next Steps
1. Choose an agent that matches your use case
2. Follow the specific setup instructions in that agent's README
3. Start with local testing before deploying to production
4. Review evaluation examples to understand expected capabilities

For detailed information about each agent, see their individual README files.