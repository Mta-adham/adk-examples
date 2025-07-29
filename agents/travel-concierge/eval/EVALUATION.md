# Travel Concierge Agent - Evaluation Guide

This guide provides step-by-step instructions for setting up and running the evaluation of the Travel Concierge agent.

## Overview

The Travel Concierge Agent is an AI-powered travel assistant built using Google's Agent Development Kit (ADK). It orchestrates personalized travel experiences, integrates booking systems, and provides support throughout the traveler's journey, from initial planning and booking to real-time itinerary services and alerts.

## Prerequisites

- Python 3.11+
- `uv` package manager
- Google Cloud Platform project with appropriate permissions
- `gcloud` CLI configured and authenticated

## Environment Setup

### 1. Install Dependencies

```bash
uv sync --all-extras
```

This installs all required dependencies including evaluation tools from the `google-adk[eval]` package.

### 2. Configure Google Cloud Credentials

Ensure you have authenticated with Google Cloud:

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project $GOOGLE_CLOUD_PROJECT
```

### 3. Create Environment Configuration

Create a `.env` file in the project root with the following variables:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=evoml-mcp
GOOGLE_CLOUD_LOCATION=us-central1
MODEL="gemini-2.5-flash"
STAGING_BUCKET=evoml-mcp
```

## Running the Evaluation

Execute the evaluation using:

```bash
uv run pytest eval -v
```

The evaluation tests three main scenarios:
- **inspire**: Tests the inspiration agent functionality
- **pretrip**: Tests pre-trip planning capabilities  
- **intrip**: Tests in-trip assistance and monitoring

## Evaluation Configuration

The evaluation runs with the following test cases:
- **Test cases**: Located in `eval/data/` directory
- **Test scenarios**: 
  - `inspire.test.json` - Travel inspiration queries
  - `pretrip.test.json` - Pre-trip agent transfers and state inspection
  - `intrip.test.json` - In-trip monitoring and assistance

## Test Results

### Latest Evaluation Results

For detailed evaluation results including test execution data and error analysis, see:

📁 **[evaluation_results/](./evaluation_results/)** directory

**Latest Results:**
- [2025-07-24 Evaluation Results](./evaluation_results/2025-07-24_evaluation-results.md) - PARTIALLY FAILED (2/3 tests passed) with KeyError in in-trip agent

## Migration Status

✅ **MIGRATION SUCCESSFUL** - Agent successfully migrated from Poetry to uv-based setup

**Migration Changes:**
- Converted from `[tool.poetry.dependencies]` format to standard `[project]` configuration
- Updated to use setuptools build system instead of poetry-core  
- Reorganized dev/deployment dependencies as `[project.optional-dependencies]`
- Created `.env.example` with proper Vertex AI and GCP bucket configuration
- All dependencies install correctly with `uv sync --all-extras`
- Maintained all original functionality and dependencies

## Success Criteria

The migrated agent demonstrates:

1. **✅ Functional Migration**: Core functionality preserved after migration
2. **✅ Environment Setup**: uv-based installation works correctly
3. **✅ Dependency Management**: All required packages install properly
4. **✅ Inspiration Agent**: Successfully provides travel inspiration
5. **✅ Pre-trip Agent**: Handles pre-trip planning and state inspection
6. **⚠️ In-trip Agent**: Partial failure due to itinerary state handling bug

## Issue Analysis

### In-trip Test Failure

The failing test reveals a robustness issue in the `_inspect_itinerary()` function:

**Current Implementation:**
```python
def _inspect_itinerary(state: dict[str: Any]):
    itinerary = state[constants.ITIN_KEY]
    profile = state[constants.PROF_KEY]  
    current_datetime = itinerary["start_date"] + " 00:00"  # Fails here
    # ...
```

**Issue**: The function assumes `start_date` key exists in itinerary without validation.

**Suggested Fix**: Add proper error handling for empty or incomplete itineraries:
```python
def _inspect_itinerary(state: dict[str: Any]):
    itinerary = state[constants.ITIN_KEY]
    profile = state[constants.PROF_KEY]
    
    # Handle empty or incomplete itinerary
    if not itinerary or "start_date" not in itinerary:
        current_datetime = "1970-01-01 00:00"  # Default fallback
    else:
        current_datetime = itinerary["start_date"] + " 00:00"
    # ...
```

## Troubleshooting

### Common Issues

1. **API Authentication Errors**
   - Verify Google Cloud credentials: `gcloud auth list`
   - Ensure Vertex AI API is enabled: `gcloud services enable aiplatform.googleapis.com`
   - Check project configuration: `gcloud config get-value project`

2. **Missing Dependencies**
   - Reinstall with all extras: `uv sync --all-extras`
   - Verify uv installation: `uv --version`

3. **In-trip Test Failures**
   - Issue is with empty itinerary state handling in test scenario
   - Function expects populated itinerary but receives empty object `{}`
   - Requires code fix in `travel_concierge/sub_agents/in_trip/tools.py`

4. **Environment Configuration**
   - Ensure `.env` file has proper GCP project and location settings
   - Verify bucket access: `gsutil ls gs://evoml-mcp/`

## Recommendations

### For Production Use

1. **Fix In-trip Agent**: Add proper error handling for empty/incomplete itinerary states
2. **Test Coverage**: Update test scenarios to include various itinerary states (empty, partial, complete)
3. **Validation**: Add itinerary validation before state-dependent operations
4. **Error Handling**: Implement graceful fallbacks when expected state keys are missing

### For Development

1. **Defensive Programming**: Add null/empty checks for all state dependencies
2. **Test Scenarios**: Create additional test cases covering edge cases
3. **Documentation**: Update function documentation to specify required state structure

## Evaluation Output Schema

### Standard Metrics

The evaluation tests three main travel workflow scenarios with standard ADK evaluation metrics:

#### Tool Trajectory Average Score
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures correctness of multi-agent coordination and travel workflow execution
- **Interpretation**:
  - 1.0 = Perfect coordination between inspiration, pre-trip, and in-trip agents
  - < 1.0 = Missing agent transfers, incorrect tool usage, or workflow coordination failures
- **Threshold**: Not explicitly defined (evaluation focuses on functional workflow completion)

#### Response Match Score
- **Type**: Float (0.0 - 1.0)
- **Description**: Measures response quality for travel assistance using ROUGE scoring
- **Interpretation**:
  - Higher values indicate better similarity to expected travel assistance responses
  - Accounts for natural variations in travel recommendations and itinerary responses
- **Threshold**: Not explicitly defined (evaluation focuses on functional workflow completion)

### Multi-Agent Travel Workflow Evaluation

The evaluation specifically tests coordination between specialized travel sub-agents:
- **Inspiration Agent**: Provides travel destination suggestions and inspiration
- **Pre-trip Agent**: Handles travel planning and preparation workflows  
- **In-trip Agent**: Manages real-time travel assistance and itinerary monitoring

### Output Format Example

```
| Test Case | Status | Details |
|-----------|--------|---------|
| test_inspire | ✅ PASSED | Travel inspiration functionality working correctly |
| test_pretrip | ✅ PASSED | Pre-trip agent transfer and basic functionality working |
| test_intrip | ❌ FAILED | KeyError: 'start_date' in itinerary inspection |

Overall Status: ⚠️ PARTIALLY FAILED (2/3 tests passed)
```

### Test Scenarios Evaluated

1. **Inspire Test** (`inspire.test.json`):
   - **Functionality**: Travel inspiration and destination suggestion
   - **Agent Transfer**: Root agent → inspiration sub-agent
   - **Result**: ✅ PASSED

2. **Pre-trip Test** (`pretrip.test.json`):
   - **Functionality**: Pre-trip planning and state inspection
   - **Agent Transfer**: Root agent → pre-trip sub-agent  
   - **Result**: ✅ PASSED

3. **In-trip Test** (`intrip.test.json`):
   - **Functionality**: In-trip monitoring and transit coordination
   - **Error**: `KeyError: 'start_date'` in `_inspect_itinerary()` function
   - **Result**: ❌ FAILED

### Error Analysis

**In-trip Test Failure Details**:
- **Location**: `travel_concierge/sub_agents/in_trip/tools.py:197`
- **Root Cause**: Function expects `itinerary["start_date"]` but receives empty itinerary `{}`
- **Impact**: Prevents in-trip monitoring and transit coordination functionality

### Success Indicators (Functional Assessment)

The migrated agent demonstrates:
- ✅ **Functional Migration**: Core functionality preserved after uv migration
- ✅ **Environment Setup**: uv-based installation works correctly  
- ✅ **Inspiration Agent**: Successfully provides travel inspiration
- ✅ **Pre-trip Agent**: Handles pre-trip planning and state inspection
- ⚠️ **In-trip Agent**: Partial failure due to itinerary state handling bug

### Performance Characteristics
- **Total Evaluation Duration**: ~216 seconds (3 minutes 37 seconds)
- **Migration Success**: ✅ Complete transition from Poetry to uv
- **Agent Architecture**: Multi-agent travel system remains intact
- **State Management**: Requires improvement for edge cases (empty itinerary handling)

### Error Handling Recommendations

**Suggested Fix for In-trip Agent**:
```python
def _inspect_itinerary(state: dict[str: Any]):
    itinerary = state[constants.ITIN_KEY]
    profile = state[constants.PROF_KEY]
    
    # Handle empty or incomplete itinerary
    if not itinerary or "start_date" not in itinerary:
        current_datetime = "1970-01-01 00:00"  # Default fallback
    else:
        current_datetime = itinerary["start_date"] + " 00:00"
```

## Conclusion

The Travel Concierge Agent migration to uv was successful, with the agent maintaining most functionality after conversion from Poetry-based dependency management. Two of three test scenarios pass completely, demonstrating working inspiration and pre-trip capabilities. 

The in-trip test failure reveals a robustness issue that should be addressed before production deployment. The core agent architecture and sub-agent system remain intact and functional, with the primary issue being insufficient error handling for edge cases in state management.

The agent demonstrates strong potential for travel assistance workflows, with the identified bug being straightforward to fix with proper error handling and validation.