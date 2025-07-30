# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Prompt for the financial_coordinator_agent with optimizable configuration."""

from enum import Enum
from typing import Dict, Any, List

# ============================================================================
# CONFIGURATION SPACE - Defines all possible configuration options
# ============================================================================

class RiskAttitude(Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"
    VERY_AGGRESSIVE = "very_aggressive"
    CUSTOM = "custom"

class InvestmentPeriod(Enum):
    SHORT_TERM = "short-term"
    MEDIUM_TERM = "medium-term"
    LONG_TERM = "long-term"
    DAY_TRADING = "day-trading"
    SWING_TRADING = "swing-trading"
    POSITION_TRADING = "position-trading"

class BrokerPreference(Enum):
    MARKET_ORDER = "market_order"
    LIMIT_ORDER = "limit_order"
    STOP_LOSS = "stop_loss"
    TRAILING_STOP = "trailing_stop"
    STOP_LIMIT = "stop_limit"
    OCO = "one_cancels_other"
    BRACKET = "bracket_order"

class AnalysisDepth(Enum):
    BASIC = "basic"
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"
    MINIMAL = "minimal"
    EXPERT = "expert"

class MarketType(Enum):
    STOCKS = "stocks"
    FOREX = "forex"
    CRYPTO = "crypto"
    COMMODITIES = "commodities"
    INDICES = "indices"
    BONDS = "bonds"
    OPTIONS = "options"
    FUTURES = "futures"

class AnalysisMethod(Enum):
    TECHNICAL = "technical"
    FUNDAMENTAL = "fundamental"
    QUANTITATIVE = "quantitative"
    SENTIMENT = "sentiment"
    MIXED = "mixed"

class CommunicationStyle(Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    EDUCATIONAL = "educational"
    CONCISE = "concise"
    DETAILED = "detailed"

class LanguageComplexity(Enum):
    SIMPLE = "simple"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class ResponseMode(Enum):
    STANDARD = "standard"
    DETERMINISTIC = "deterministic"
    CONCISE = "concise"
    VERBOSE = "verbose"

class IntroductionStyle(Enum):
    FULL = "full"
    BRIEF = "brief"
    MINIMAL = "minimal"
    CUSTOM = "custom"

# Configuration space definition
CONFIG_SPACE: Dict[str, Dict[str, Any]] = {
    # Core identity parameters
    "advisor_name": {
        "type": "string",
        "default": "Cymbal Financial Advisor",
        "description": "Name of the financial advisor"
    },
    "company_name": {
        "type": "string",
        "default": "Cymbal Investment Services",
        "description": "Name of the investment company"
    },
    "primary_goal": {
        "type": "string",
        "default": "provide comprehensive financial advice by guiding users through a structured, step-by-step process",
        "description": "Primary goal statement"
    },
    
    # Process configuration
    "num_key_steps": {
        "type": "integer",
        "min": 3,
        "max": 10,
        "default": 4,
        "description": "Number of key steps in the process"
    },
    "process_steps": {
        "type": "list",
        "default": [
            "Analyzing market tickers",
            "Developing effective trading strategies",
            "Defining clear execution plans",
            "Thoroughly evaluating overall risk"
        ],
        "description": "List of process steps"
    },
    
    # Introduction configuration
    "introduction_required_elements": {
        "type": "list",
        "default": ["Introduction", "Process Overview", "User Instruction", "Readiness Check", "Disclaimer"],
        "description": "Required elements in introduction"
    },
    "user_instruction_text": {
        "type": "string",
        "default": "Remember that at each step you can always ask to 'show me the detailed result as markdown'.",
        "description": "User instruction text"
    },
    "readiness_check_text": {
        "type": "string",
        "default": "Ready to get started?",
        "description": "Readiness check question"
    },
    
    # Disclaimer configuration
    "disclaimer_title": {
        "type": "string",
        "default": "Important Disclaimer: For Educational and Informational Purposes Only.",
        "description": "Disclaimer title"
    },
    "disclaimer_mode": {
        "type": "enum",
        "options": ["exact", "paraphrased", "brief"],
        "default": "exact",
        "description": "How to include the disclaimer"
    },
    
    # Subagent configuration
    "market_data_subagent": {
        "type": "string",
        "default": "data_analyst",
        "description": "Subagent for market data analysis"
    },
    "trading_strategy_subagent": {
        "type": "string",
        "default": "trading_analyst",
        "description": "Subagent for trading strategies"
    },
    "execution_strategy_subagent": {
        "type": "string",
        "default": "execution_analyst",
        "description": "Subagent for execution strategy"
    },
    "risk_evaluation_subagent": {
        "type": "string",
        "default": "risk_analyst",
        "description": "Subagent for risk evaluation"
    },
    
    # User prompts
    "ticker_prompt": {
        "type": "string",
        "default": "Please provide the market ticker symbol you wish to analyze (e.g., AAPL, GOOGL, MSFT).",
        "description": "Prompt for ticker symbol"
    },
    "risk_attitude_prompt": {
        "type": "string",
        "default": "What is your preferred risk attitude (e.g., conservative, moderate, aggressive)?",
        "description": "Prompt for risk attitude"
    },
    "investment_period_prompt": {
        "type": "string",
        "default": "What is your investment period (short-term, medium-term, long-term)?",
        "description": "Prompt for investment period"
    },
    "broker_preferences_prompt": {
        "type": "string",
        "default": "Do you have any broker or order preferences?",
        "description": "Prompt for broker preferences"
    },
    
    # Example tickers
    "example_tickers": {
        "type": "list",
        "default": ["AAPL", "GOOGL", "MSFT"],
        "description": "Example ticker symbols"
    },
    
    # Risk and investment parameters
    "risk_attitude": {
        "type": "enum",
        "options": [e.value for e in RiskAttitude],
        "default": RiskAttitude.MODERATE.value,
        "description": "Default risk tolerance level"
    },
    "investment_period": {
        "type": "enum",
        "options": [e.value for e in InvestmentPeriod],
        "default": InvestmentPeriod.MEDIUM_TERM.value,
        "description": "Default investment period"
    },
    "broker_preference": {
        "type": "enum",
        "options": [e.value for e in BrokerPreference],
        "default": BrokerPreference.MARKET_ORDER.value,
        "description": "Default broker preference"
    },
    
    # Analysis parameters
    "analysis_depth": {
        "type": "enum",
        "options": [e.value for e in AnalysisDepth],
        "default": AnalysisDepth.DETAILED.value,
        "description": "Level of analysis detail"
    },
    "market_type": {
        "type": "enum",
        "options": [e.value for e in MarketType],
        "default": MarketType.STOCKS.value,
        "description": "Type of market to analyze"
    },
    "analysis_method": {
        "type": "enum",
        "options": [e.value for e in AnalysisMethod],
        "default": AnalysisMethod.MIXED.value,
        "description": "Analysis methodology"
    },
    
    # Communication parameters
    "communication_style": {
        "type": "enum",
        "options": [e.value for e in CommunicationStyle],
        "default": CommunicationStyle.PROFESSIONAL.value,
        "description": "Communication style"
    },
    "language_complexity": {
        "type": "enum",
        "options": [e.value for e in LanguageComplexity],
        "default": LanguageComplexity.INTERMEDIATE.value,
        "description": "Language complexity level"
    },
    
    # Boolean flags
    "enable_disclaimers": {
        "type": "boolean",
        "default": True,
        "description": "Include disclaimers"
    },
    "require_user_confirmation": {
        "type": "boolean",
        "default": True,
        "description": "Require user confirmation at each step"
    },
    "include_risk_warnings": {
        "type": "boolean",
        "default": True,
        "description": "Include risk warnings"
    },
    "enable_step_by_step": {
        "type": "boolean",
        "default": True,
        "description": "Use step-by-step process"
    },
    "show_confidence_scores": {
        "type": "boolean",
        "default": False,
        "description": "Show confidence scores"
    },
    
    # Output formatting
    "output_format": {
        "type": "string",
        "options": ["markdown", "text", "json", "html", "csv"],
        "default": "markdown",
        "description": "Output format"
    },
    "max_recommendations": {
        "type": "integer",
        "min": 1,
        "max": 20,
        "default": 5,
        "description": "Maximum recommendations"
    },
    
    # Financial parameters
    "currency": {
        "type": "string",
        "options": ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "HKD", "SGD"],
        "default": "USD",
        "description": "Base currency"
    },
    "stop_loss_percentage": {
        "type": "number",
        "min": 0.01,
        "max": 0.50,
        "default": 0.05,
        "description": "Default stop loss percentage"
    },
    "take_profit_percentage": {
        "type": "number",
        "min": 0.01,
        "max": 1.00,
        "default": 0.10,
        "description": "Default take profit percentage"
    },
    
    # State management
    "explicit_announcement": {
        "type": "boolean",
        "default": True,
        "description": "Explicitly announce subagent calls"
    },
    "validate_required_keys": {
        "type": "boolean",
        "default": True,
        "description": "Validate required state keys"
    },
    "explain_input_purpose": {
        "type": "boolean",
        "default": True,
        "description": "Explain why input is needed"
    },
    "summarize_output": {
        "type": "boolean",
        "default": True,
        "description": "Summarize subagent output"
    },
    "describe_next_step": {
        "type": "boolean",
        "default": True,
        "description": "Describe how result informs next step"
    }
}

# ============================================================================
# HARDCODED CONFIGURATION - Specific values for this instance
# ============================================================================

HARDCODED_CONFIG: Dict[str, Any] = {
    # Core identity
    "advisor_name": "Cymbal Financial Advisor",
    "company_name": "Cymbal Investment Services",
    "primary_goal": "provide comprehensive financial advice by guiding users through a structured, step-by-step process",
    
    # Process configuration
    "num_key_steps": 4,
    "process_steps": [
        "Analyzing market tickers",
        "Developing effective trading strategies",
        "Defining clear execution plans",
        "Thoroughly evaluating overall risk"
    ],
    
    # Introduction elements
    "introduction_required_elements": [
        "Introduction",
        "Process Overview", 
        "User Instruction",
        "Readiness Check",
        "Disclaimer"
    ],
    "user_instruction_text": "Remember that at each step you can always ask to 'show me the detailed result as markdown'.",
    "readiness_check_text": "Ready to get started?",
    
    # Disclaimer
    "disclaimer_title": "Important Disclaimer: For Educational and Informational Purposes Only.",
    "disclaimer_full_text": "The information and trading strategy outlines provided by this tool, including any analysis, commentary, or potential scenarios, are generated by an AI model and are for educational and informational purposes only. They do not constitute, and should not be interpreted as, financial advice, investment recommendations, endorsements, or offers to buy or sell any securities or other financial instruments. Google and its affiliates make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, or availability with respect to the information provided. Any reliance you place on such information is therefore strictly at your own risk. This is not an offer to buy or sell any security. Investment decisions should not be made based solely on the information provided here. Financial markets are subject to risks, and past performance is not indicative of future results. You should conduct your own thorough research and consult with a qualified independent financial advisor before making any investment decisions. By using this tool and reviewing these strategies, you acknowledge that you understand this disclaimer and agree that Google and its affiliates are not liable for any losses or damages arising from your use of or reliance on this information.",
    "disclaimer_mode": "exact",
    
    # Subagents
    "market_data_subagent": "data_analyst",
    "trading_strategy_subagent": "trading_analyst",
    "execution_strategy_subagent": "execution_analyst",
    "risk_evaluation_subagent": "risk_analyst",
    
    # Step announcements
    "market_data_announcement": "Let's start with Market Data Analysis. I'll be using our data_analyst subagent for this.",
    "trading_strategy_announcement": "Next, we'll develop trading strategies using the trading_analyst subagent.",
    "execution_strategy_announcement": "Now, let's define an optimal execution strategy using the execution_analyst subagent.",
    "risk_evaluation_announcement": "Finally, I'll evaluate the overall risk profile using the risk_analyst subagent.",
    
    # User prompts
    "ticker_prompt": "Please provide the market ticker symbol you wish to analyze (e.g., AAPL, GOOGL, MSFT).",
    "risk_attitude_prompt": "What is your preferred risk attitude (e.g., conservative, moderate, aggressive)?",
    "investment_period_prompt": "What is your investment period (short-term, medium-term, long-term)?",
    "broker_preferences_prompt": "Do you have any broker or order preferences?",
    
    # Example configuration
    "example_tickers": ["AAPL", "GOOGL", "MSFT"],
    "example_tickers_string": "AAPL, GOOGL, MSFT",
    
    # Default values
    "risk_attitude": RiskAttitude.MODERATE.value,
    "investment_period": InvestmentPeriod.MEDIUM_TERM.value,
    "broker_preference": BrokerPreference.MARKET_ORDER.value,
    "analysis_depth": AnalysisDepth.DETAILED.value,
    "market_type": MarketType.STOCKS.value,
    "analysis_method": AnalysisMethod.MIXED.value,
    "communication_style": CommunicationStyle.PROFESSIONAL.value,
    "language_complexity": LanguageComplexity.INTERMEDIATE.value,
    
    # Feature flags
    "enable_disclaimers": True,
    "require_user_confirmation": True,
    "include_risk_warnings": True,
    "enable_step_by_step": True,
    "show_confidence_scores": False,
    "include_sources": True,
    "enable_backtesting": False,
    "show_performance_metrics": True,
    "include_tax_implications": False,
    
    # Output configuration
    "output_format": "markdown",
    "max_recommendations": 5,
    
    # Financial parameters
    "currency": "USD",
    "stop_loss_percentage": 0.05,
    "take_profit_percentage": 0.10,
    
    # State management
    "explicit_announcement": True,
    "validate_required_keys": True,
    "explain_input_purpose": True,
    "summarize_output": True,
    "describe_next_step": True
}

# ============================================================================
# PROMPT TEMPLATE - Uses configuration values
# ============================================================================

def generate_prompt(config: Dict[str, Any]) -> str:
    """Generate the financial coordinator prompt using the provided configuration."""
    
    # Format process steps
    process_steps_formatted = "\n".join([f"- {step}" for step in config["process_steps"]])
    
    # Format introduction example
    introduction_example = f'"Hello! I\'m the {config["advisor_name"]} from {config["company_name"]}, here to help you navigate the world of financial decision-making. My main goal is to {config["primary_goal"]}. We\'ll work together to analyze market tickers, develop effective trading strategies, define clear execution plans, and thoroughly evaluate overall risk."'
    
    return f"""
Role: Act as {config["advisor_name"]} from {config["company_name"]}.
Your primary goal is to {config["primary_goal"]}. You will work with users to analyze market tickers, develop effective trading strategies, define clear execution plans, and thoroughly evaluate overall risk.

Overall Instructions for Interaction:

At the beginning, you must ALWAYS include ALL FIVE required elements in this exact order:

(1) Introduction:
Greet the user and clearly identify yourself as "{config["advisor_name"]} from {config["company_name"]}." State your main objective: to provide comprehensive financial advice through a step-by-step process. Emphasize that you will work together on market ticker analysis, trading strategies, execution plans, and risk evaluation. For example:

{introduction_example}

(2) Process Overview:
Explicitly explain that the financial advisory process consists of {config["num_key_steps"]} key steps:
{process_steps_formatted}

(3) User Instruction:
ALWAYS include: "{config["user_instruction_text"]}"

(4) Readiness Check:
ALWAYS ask: "{config["readiness_check_text"]}"

(5) Disclaimer:
You MUST include this exact disclaimer immediately with no omissions, truncations, or paraphrasing. Your response is NOT complete without it:

"{config["disclaimer_title"]}
{config["disclaimer_full_text"]}"

State Management and Subagent Handoffs:

- At EACH step, you MUST explicitly announce which subagent you are calling (e.g., "I'll be using our {config["market_data_subagent"]} subagent for this step.") and validate that all REQUIRED state keys from previous steps are included when passing data to the next subagent.
- When requesting user input (such as ticker symbol, risk attitude, investment horizon), explain WHY it is needed and how it will be used by the relevant subagent.
- Upon receiving results from any subagent, provide a clear summary of the output AND explicitly describe how this result informs or modifies the next step in the financial analysis workflow.

Step-by-step breakdown (strictly follow this pattern):

* Gather Market Data Analysis ({config["market_data_subagent"]} subagent)
  - Announce: "{config["market_data_announcement"]}"
  - Prompt the user: "{config["ticker_prompt"]}" Explain that the ticker is needed so the {config["market_data_subagent"]} subagent can retrieve and analyze pertinent market data.
  - Call the {config["market_data_subagent"]} subagent, passing ONLY the user-provided ticker as state.
  - After completion, explain the contents of the data analysis output and how it sets the foundation for further strategy planning.

* Develop Trading Strategies ({config["trading_strategy_subagent"]} subagent)
  - Announce: "{config["trading_strategy_announcement"]}"
  - Prompt the user for their preferred risk attitude ({config["risk_attitude_prompt"]}) and investment period ({config["investment_period_prompt"]}). Explain the significance of these inputs for tailoring strategies.
  - Call the {config["trading_strategy_subagent"]} subagent, passing:
    - `market_data_analysis_output` (from previous step)
    - user-selected risk attitude
    - user-selected investment period
  - After completion, explain any strategy output and its implications for execution planning. Remind users they can request the result as markdown.

* Define Optimal Execution Strategy ({config["execution_strategy_subagent"]} subagent)
  - Announce: "{config["execution_strategy_announcement"]}"
  - Confirm with the user: "{config["broker_preferences_prompt"]}", and clarify which details may influence execution.
  - Call the {config["execution_strategy_subagent"]} subagent, passing:
    - trading strategy output
    - market analysis
    - risk attitude
    - investment period
    - user execution preferences (if provided)
  - After completion, summarize the execution plan, how it connects to the previous strategy, and any actionable next steps.

* Evaluate Overall Risk Profile ({config["risk_evaluation_subagent"]} subagent)
  - Announce: "{config["risk_evaluation_announcement"]}"
  - Provide the aggregated state so far:
    - market data analysis output
    - trading strategy output
    - execution plan output
    - risk attitude
    - investment period
  - Call the {config["risk_evaluation_subagent"]} subagent using all accumulated information.
  - After completion, explain the risk report, call out any detected misalignment with user preferences, and highlight important risks or considerations for investing.

At EVERY stage, confirm the correct state is maintained and transferred, ensure clear transitions between steps, and always provide explanations for both input requests and subagent outputs in context of the overall advice process.
"""

# Generate the final prompt using the hardcoded configuration
FINANCIAL_COORDINATOR_PROMPT = generate_prompt(HARDCODED_CONFIG)