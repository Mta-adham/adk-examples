# Personalized Shopping Agent Evaluation Guide

This guide provides instructions for setting up and running the evaluation tests for the Personalized Shopping Agent built using Google's Agent Development Kit (ADK).

## Overview

The Personalized Shopping Agent is an AI-powered assistant that helps users find products through a simulated e-commerce environment. It uses the WebShop environment from [princeton-nlp/WebShop](https://github.com/princeton-nlp/WebShop) with real-world product data and provides personalized shopping recommendations.

## Prerequisites

- Python 3.11-3.12 (Note: Python 3.13+ not supported due to pyjnius compatibility)
- uv (for dependency management)
- Java 11+ (required for Apache Lucene search engine)
- Google Cloud Project with Vertex AI enabled, or Google Gemini API key
- Google Cloud SDK (if using Vertex AI)

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

Edit the `.env` file with one of the following configurations:

**Option A: Google Cloud Vertex AI (Recommended)**
```env
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_STORAGE_BUCKET=your-storage-bucket
```

**Option B: Google Gemini Developer API**
```env
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your-gemini-api-key
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_STORAGE_BUCKET=your-storage-bucket
```

### 3. Authenticate (if using Vertex AI)

```bash
gcloud auth application-default login --project=your-project-id
gcloud services enable aiplatform.googleapis.com
```

### 4. WebShop Environment Setup

The agent requires the WebShop environment with product data and search indexes. This is the most complex part of the setup:

#### Download Product Data

```bash
cd personalized_shopping/shared_libraries
mkdir -p data
cd data

# Download required product data files
uv run gdown https://drive.google.com/uc?id=1EgHdxQ_YxqIQlvvq5iKlCrkEKR6-j0Ib  # items_shuffle_1000.json (4.5MB)
uv run gdown https://drive.google.com/uc?id=1IduG0xl544V_A_jv3tHXC0kyFi7PnyBu  # items_ins_v2_1000.json (147KB)
uv run gdown https://drive.google.com/uc?id=14Kb5SPBk_jfdLZ_CDBNitW98QLDlKR5O  # items_human_ins.json (4.9MB)

# Optional: Download larger datasets (for production use)
# uv run gdown https://drive.google.com/uc?id=1A2whVgOO0euk5O13n2iYDM0bQRkkRduB  # items_shuffle.json (5.1GB)
# uv run gdown https://drive.google.com/uc?id=1s2j6NgHljiZzQNL3veZaAiyW_qDEgBNi  # items_ins_v2.json (178MB)
```

#### Setup Search Engine Indexes

```bash
cd ../search_engine
mkdir -p resources_100 resources_1k resources_10k resources_50k

# Convert product files to Lucene format
uv run python convert_product_file_format.py

# Create search indexes (requires Java)
mkdir -p indexes
bash run_indexing.sh
```

**Note**: The indexing process requires Java and may encounter compatibility issues with newer Java versions or the `jdk.incubator.vector` module.

## Running the Evaluation

Execute the evaluation tests using pytest:

```bash
uv run pytest eval -v
```

## Evaluation Test Cases

The evaluation consists of a simple test scenario:

### Simple Test (`simple.test.json`)
Tests basic agent functionality with a single interaction:
- **Greeting**: "Hello, who are you?" - Tests agent introduction and capability description

## Evaluation Metrics

The evaluation uses two key metrics defined in `test_config.json`:

1. **Tool Trajectory Average Score**: Measures correctness of tool usage (expected threshold: 1.0)
2. **Response Match Score**: Measures response quality using ROUGE scoring (expected threshold: 0.6)

## Known Issues and Limitations

### Setup Complexity
The WebShop environment setup is complex and requires:
- Large dataset downloads (up to 5GB for full dataset)
- Java-based search engine indexing
- Compatibility issues with newer Java versions

### Java Compatibility
The agent relies on pyserini (Python wrapper for Apache Lucene) which requires:
- Java 11+ runtime
- Specific Java modules that may not be available in all environments
- May encounter `Module jdk.incubator.vector not found` errors

### Performance Considerations
- First run initialization can take significant time loading 50,000+ products
- Search indexing requires substantial disk space and processing time
- Agent response times depend on search engine performance

## Simplified Evaluation Setup

For basic testing without full WebShop setup, you can:

1. Reduce the product dataset size in `init_env.py`:
   ```python
   num_product_items = 1000  # Instead of 50000
   ```

2. Use the 1000-item datasets instead of full datasets

3. Focus on testing agent responses without tool functionality

## Troubleshooting

### Common Issues

1. **Java Module Errors**
   ```
   Error occurred during initialization of boot layer
   java.lang.module.FindException: Module jdk.incubator.vector not found
   ```
   **Solution**: Try using Java 11 instead of newer versions, or consider alternative search implementations.

2. **Missing Product Data**
   ```
   FileNotFoundError: items_shuffle.json not found
   ```
   **Solution**: Ensure all required data files are downloaded to the correct directory.

3. **Missing Dependencies**
   ```
   ModuleNotFoundError: No module named 'pytest_asyncio'
   ```
   **Solution**: Install all extras with `uv sync --all-extras`

4. **Long Initialization Times**
   - The agent initializes a WebShop environment with thousands of products
   - First run may take several minutes
   - Consider reducing `num_product_items` for faster testing

### Environment Reset

If evaluation fails due to corrupted state:

```bash
# Clean up and restart
rm -rf .venv
uv sync --all-extras
# Re-download data files if needed
```

## Expected Results

**Note**: Due to setup complexity, complete evaluation results depend on successful WebShop environment initialization.

### Successful Evaluation Output
When properly configured, the evaluation should demonstrate:
- ✅ Agent correctly identifies itself as a webshop agent
- ✅ Agent describes its product search and recommendation capabilities
- ✅ Response quality meets similarity thresholds
- ✅ Basic conversational flow works correctly

### Partial Success Scenarios
If WebShop environment setup fails:
- Agent may still provide valid responses about its capabilities
- Some tool functionality tests may be skipped
- Response quality evaluation may still function

## Production Deployment

For production use:
1. Complete the full WebShop environment setup with all datasets
2. Optimize search indexes for your specific product catalog
3. Consider implementing caching for frequently accessed products
4. Monitor Java memory usage and performance

## Evaluation Output Schema

### Standard Metrics

The evaluation uses two key metrics defined in `test_config.json`:

#### Tool Trajectory Average Score
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures correctness of WebShop environment interaction and product search tool usage
- **Interpretation**:
  - 1.0 = Perfect tool usage with correct WebShop navigation and product search
  - < 1.0 = Missing tool calls, incorrect WebShop interactions, or search failures
- **Threshold**: 1.0 (defined in `eval/eval_data/test_config.json`)

#### Response Match Score
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures response quality using ROUGE scoring for e-commerce assistance responses
- **Interpretation**:
  - 0.6+ = High-quality e-commerce assistance with proper product recommendations
  - 0.4-0.6 = Acceptable shopping assistance responses
  - < 0.4 = Insufficient response quality for e-commerce scenarios
- **Threshold**: 0.6 (defined in `eval/eval_data/test_config.json`)

### WebShop Environment Integration

The evaluation specifically tests integration with the WebShop environment featuring:
- **Product Database**: 50,000+ real-world products (or 1,000 for simplified setup)
- **Search Engine**: Apache Lucene-based product search with Java integration
- **Product Categories**: Various e-commerce categories with detailed product information
- **Recommendation System**: Personalized shopping assistance capabilities

### Output Format Example

```
✅ Agent Self-Identification: Correctly identifies as webshop agent
✅ Capability Description: Describes product search and recommendation capabilities  
✅ Response Quality: Meets similarity thresholds for conversational flow
✅ WebShop Integration: Successfully initializes product search environment (when configured)
```

### Test Scenario Evaluated

**Simple Test** (`simple.test.json`):
- **Query**: "Hello, who are you?" 
- **Expected**: Agent introduction explaining webshop capabilities
- **Validation**: Tests basic agent identity and capability description

### Success Indicators (When Fully Configured)
- ✅ **Agent Identity**: Correctly identifies itself as a webshop agent
- ✅ **Capability Description**: Accurately describes product search and recommendation features
- ✅ **WebShop Environment**: Successfully loads product database and search indexes
- ✅ **Product Search**: Functional integration with Apache Lucene search engine
- ✅ **Conversational Flow**: Natural dialogue for e-commerce assistance

### Setup Complexity Considerations

**Full Environment Requirements**:
- Large dataset downloads (up to 5GB for complete product catalog)
- Java 11+ runtime for Apache Lucene search engine
- Complex indexing process for 50,000+ products
- Substantial disk space and processing time for first initialization

**Simplified Evaluation**:
- Reduced to 1,000 products for faster testing
- Focus on agent responses without full tool functionality
- Basic conversational capabilities without complete WebShop setup

### Performance Characteristics
- **First Run Initialization**: Several minutes with full product dataset
- **Response Time**: Depends on search engine performance and product database size
- **Memory Usage**: Significant due to product database and search indexes
- **Java Dependency**: Requires compatible Java version for pyserini integration

## Conclusion

The Personalized Shopping Agent provides a sophisticated e-commerce assistance experience when properly configured. While the evaluation setup is complex due to the WebShop environment requirements, the agent demonstrates strong conversational abilities and product search integration. The evaluation framework provides comprehensive metrics for both response quality and tool usage effectiveness.

For development and testing purposes, consider using the simplified setup with reduced datasets to focus on core agent functionality without the full complexity of the WebShop environment.