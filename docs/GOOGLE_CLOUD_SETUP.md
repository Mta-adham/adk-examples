# Google Cloud Project Setup Guide for ADK Agents

This guide walks you through setting up a Google Cloud project using the gcloud CLI to run all 11 ADK agents in this repository.

## Prerequisites

- Install [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
- Have a Google account with billing capabilities

## 1. Initial Project Setup

### Create a New Project
```bash
# Set your desired project ID (must be globally unique)
# Note: Project IDs can be 6-30 characters, lowercase letters, numbers, and hyphens only
export PROJECT_ID="your-adk-agents-project"

# Create the project
# Note: Project display name must be 30 characters or less
gcloud projects create $PROJECT_ID --name="ADK Agents Project"

# Set as default project for gcloud commands
gcloud config set project $PROJECT_ID
```

### Enable Billing
```bash
# List available billing accounts
gcloud billing accounts list

# Link billing account to project (replace BILLING_ACCOUNT_ID)
gcloud billing projects link $PROJECT_ID --billing-account=BILLING_ACCOUNT_ID
```

### Verify Project Setup
```bash
# Confirm project is active and billing is enabled
gcloud projects describe $PROJECT_ID
gcloud billing projects describe $PROJECT_ID
```

## 2. Authentication Setup

### Configure Application Default Credentials
```bash
# Authenticate for local development
gcloud auth application-default login

# Set quota project (recommended for API usage tracking)
gcloud auth application-default set-quota-project $PROJECT_ID
```

### Verify Authentication
```bash
# Test authentication
gcloud auth application-default print-access-token
```

## 3. Enable Required APIs

### Core AI Platform Services
```bash
# Essential for all agents
gcloud services enable aiplatform.googleapis.com
gcloud services enable generativelanguage.googleapis.com

# Additional core services
gcloud services enable compute.googleapis.com
gcloud services enable iam.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

### Agent-Specific Services
```bash
# For Data Science and Brand Search Optimization agents
gcloud services enable bigquery.googleapis.com

# For Image Scoring, deployment artifacts, and general storage
gcloud services enable storage.googleapis.com

# For Travel Concierge agent
gcloud services enable places.googleapis.com

# For advanced ML features (RAG, custom models)
gcloud services enable ml.googleapis.com
gcloud services enable discoveryengine.googleapis.com

# For potential web scraping and Chrome WebDriver usage
gcloud services enable compute.googleapis.com
```

### Verify APIs are Enabled
```bash
# List all enabled services
gcloud services list --enabled --filter="name:aiplatform OR name:bigquery OR name:storage OR name:places"
```

## 4. IAM and Service Account Setup

### Get Project Number (needed for service accounts)
```bash
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
echo "Project Number: $PROJECT_NUMBER"
```

### Grant AI Platform Permissions for Deployment
```bash
# Required for Vertex AI Agent Engine deployment
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Additional permissions for comprehensive agent functionality
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"
```

### Create Custom Service Account (Optional)
```bash
# Create service account for agent operations
gcloud iam service-accounts create adk-agents-sa \
    --display-name="ADK Agents Service Account" \
    --description="Service account for running ADK agents"

# Grant necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:adk-agents-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:adk-agents-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:adk-agents-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"
```

## 5. Agent-Specific Setup

### Cloud Storage Buckets
```bash
# Create bucket for general agent artifacts
gsutil mb gs://${PROJECT_ID}-agent-artifacts

# Create bucket for image scoring agent
gsutil mb gs://${PROJECT_ID}-image-scoring

# Set appropriate permissions
gsutil iam ch serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com:roles/storage.admin gs://${PROJECT_ID}-agent-artifacts
gsutil iam ch serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com:roles/storage.admin gs://${PROJECT_ID}-image-scoring
```

### BigQuery Setup (for Data Science and Brand Search agents)
```bash
# Create datasets for agent data
bq mk --dataset --location=us-central1 ${PROJECT_ID}:agent_analytics
bq mk --dataset --location=us-central1 ${PROJECT_ID}:brand_search_data

# Verify datasets created
bq ls
```

### Request Vertex AI Imagen Access
```bash
# Note: This requires manual approval from Google
echo "Visit https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview to request Imagen access"
echo "This is required for the Image Scoring agent"
```

## 6. Environment Configuration

### Create Base Environment Variables
```bash
# Create a template .env file that can be copied to each agent
cat > .env.template << 'EOF'
GOOGLE_CLOUD_PROJECT=PROJECT_ID_PLACEHOLDER
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=1
EOF

# Replace placeholder with actual project ID
sed "s/PROJECT_ID_PLACEHOLDER/$PROJECT_ID/g" .env.template > .env.base
```

## 7. Verification and Testing

### Test Core AI Platform Access
```bash
# Test Vertex AI access
gcloud ai models list --region=us-central1

# Test if you can create a simple AI Platform job
gcloud ai custom-jobs create \
    --region=us-central1 \
    --display-name=test-connection \
    --config=<(echo '{
        "workerPoolSpecs": [{
            "machineSpec": {"machineType": "n1-standard-4"},
            "replicaCount": 1,
            "containerSpec": {
                "imageUri": "gcr.io/cloud-aiplatform/training/tf-gpu.2-8:latest",
                "command": ["echo", "Connection test successful"]
            }
        }]
    }') || echo "Custom jobs not available, but core connection works"
```

### Test BigQuery Access
```bash
# Simple query to test BigQuery
bq query --use_legacy_sql=false 'SELECT 1 as test_connection'
```

### Test Cloud Storage Access
```bash
# Test storage access
echo "test" | gsutil cp - gs://${PROJECT_ID}-agent-artifacts/connection-test.txt
gsutil cat gs://${PROJECT_ID}-agent-artifacts/connection-test.txt
gsutil rm gs://${PROJECT_ID}-agent-artifacts/connection-test.txt
```

### Verify All Services
```bash
# Comprehensive service check
echo "=== Enabled Services ==="
gcloud services list --enabled --filter="name:aiplatform OR name:bigquery OR name:storage OR name:places OR name:generativelanguage"

echo -e "\n=== Project Configuration ==="
gcloud config list

echo -e "\n=== Storage Buckets ==="
gsutil ls

echo -e "\n=== BigQuery Datasets ==="
bq ls

echo -e "\n=== IAM Policy (AI Platform) ==="
gcloud projects get-iam-policy $PROJECT_ID --flatten="bindings[].members" --format="table(bindings.role,bindings.members)" --filter="bindings.members:*aiplatform*"
```

## 8. Agent Deployment Preparation

### Set Up Deployment Configuration
```bash
# Create deployment configuration directory
mkdir -p deployment-config

# Create a deployment settings file
cat > deployment-config/settings.yaml << EOF
project_id: $PROJECT_ID
location: us-central1
artifact_bucket: ${PROJECT_ID}-agent-artifacts
image_bucket: ${PROJECT_ID}-image-scoring
bigquery_dataset: agent_analytics
EOF
```

## 9. Next Steps

After completing this setup:

1. **Copy environment configuration**: Use `.env.base` as a template for each agent's `.env` file
2. **Install agent dependencies**: Navigate to each agent directory and run `pip install -e .`
3. **Run agent tests**: Execute `python -m pytest tests/` in each agent directory
4. **Deploy agents**: Use the deployment scripts in each agent's `deployment/` directory

## Troubleshooting

### Common Issues and Solutions

**"Permission denied" errors:**
```bash
gcloud auth application-default login
```

**"Quota exceeded" errors:**
```bash
gcloud auth application-default set-quota-project $PROJECT_ID
```

**"Service not enabled" errors:**
```bash
# Re-run the API enablement commands
gcloud services enable aiplatform.googleapis.com generativelanguage.googleapis.com
```

**"Billing not enabled" errors:**
```bash
# Check billing status
gcloud billing projects describe $PROJECT_ID
# Re-link billing if needed
gcloud billing projects link $PROJECT_ID --billing-account=YOUR_BILLING_ACCOUNT_ID
```

### Getting Help

- Check [Google Cloud documentation](https://cloud.google.com/docs)
- Review individual agent README files for specific requirements
- Use `gcloud help COMMAND` for detailed command information

## Cost Management

### Monitor Usage
```bash
# Set up billing alerts (requires Billing API)
gcloud services enable billingbudgets.googleapis.com

# Create a budget alert at $50
gcloud billing budgets create \
    --billing-account=YOUR_BILLING_ACCOUNT_ID \
    --display-name="ADK Agents Budget" \
    --budget-amount=50USD \
    --threshold-rule=percent=50,basis=CURRENT_SPEND \
    --threshold-rule=percent=90,basis=CURRENT_SPEND \
    --threshold-rule=percent=100,basis=CURRENT_SPEND
```

### Resource Cleanup
```bash
# When you're done testing, clean up resources to avoid charges:

# Delete BigQuery datasets
bq rm -r -d ${PROJECT_ID}:agent_analytics
bq rm -r -d ${PROJECT_ID}:brand_search_data

# Delete storage buckets
gsutil rm -r gs://${PROJECT_ID}-agent-artifacts
gsutil rm -r gs://${PROJECT_ID}-image-scoring

# Optionally delete the entire project
# gcloud projects delete $PROJECT_ID
```

Your Google Cloud project is now ready to run all ADK agents!