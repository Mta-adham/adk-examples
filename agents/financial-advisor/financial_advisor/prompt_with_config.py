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

"""Prompt for the financial_coordinator_agent."""

from enum import Enum
from typing import Dict, Any

# Configuration enums with available options
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

# Static configuration with default values
DEFAULT_CONFIG: Dict[str, Any] = {
    "risk_attitude": RiskAttitude.MODERATE.value,
    "investment_period": InvestmentPeriod.MEDIUM_TERM.value,
    "broker_preference": BrokerPreference.MARKET_ORDER.value,
    "analysis_depth": AnalysisDepth.DETAILED.value,
    "market_type": MarketType.STOCKS.value,
    "analysis_method": AnalysisMethod.MIXED.value,
    "communication_style": CommunicationStyle.PROFESSIONAL.value,
    "language_complexity": LanguageComplexity.INTERMEDIATE.value,
    "enable_disclaimers": True,
    "require_user_confirmation": True,
    "output_format": "markdown",
    "max_recommendations": 5,
    "include_risk_warnings": True,
    "enable_step_by_step": True,
    "show_confidence_scores": False,
    "include_sources": True,
    "enable_backtesting": False,
    "show_performance_metrics": True,
    "include_tax_implications": False,
    "currency": "USD",
    "timezone": "EST",
    "update_frequency": "real-time",
    "portfolio_size_limit": 10,
    "min_trade_size": 100,
    "max_position_size": 0.25,
    "stop_loss_percentage": 0.05,
    "take_profit_percentage": 0.10,
    "enable_notifications": False,
    "save_history": True,
    "export_format": "pdf",
    # Test-friendly configurations
    "response_mode": ResponseMode.STANDARD.value,
    "introduction_style": IntroductionStyle.FULL.value,
    "use_exact_phrases": False,
    "randomize_greetings": True,
    "include_timestamp": False,
    "use_numbered_steps": True,
    "enforce_disclaimer_format": True,
    "subagent_announcement_style": "explicit",
    "state_validation_level": "strict",
    "error_handling_verbosity": "standard",
    "test_mode": False,
    "response_template_version": "v1",
    "greeting_variations": True,
    "step_transition_phrases": "standard",
    "markdown_formatting_style": "github",
    "quote_style": "smart",
    "line_break_style": "unix",
    "max_response_length": 5000,
    "min_response_length": 50,
    "allow_emoji": False,
    "punctuation_style": "standard",
    "capitalization_style": "sentence",
    "number_format": "comma",
    "date_format": "ISO",
    "enforce_grammar_check": True,
    "allow_abbreviations": True,
    "technical_term_handling": "explain_first_use"
}

# Configuration options dictionary
CONFIG_OPTIONS: Dict[str, Dict[str, Any]] = {
    "risk_attitude": {
        "type": "enum",
        "options": [e.value for e in RiskAttitude],
        "default": RiskAttitude.MODERATE.value,
        "description": "User's risk tolerance level for investment decisions"
    },
    "investment_period": {
        "type": "enum", 
        "options": [e.value for e in InvestmentPeriod],
        "default": InvestmentPeriod.MEDIUM_TERM.value,
        "description": "Expected time horizon for investment strategy"
    },
    "broker_preference": {
        "type": "enum",
        "options": [e.value for e in BrokerPreference],
        "default": BrokerPreference.MARKET_ORDER.value,
        "description": "Preferred order execution type"
    },
    "analysis_depth": {
        "type": "enum",
        "options": [e.value for e in AnalysisDepth],
        "default": AnalysisDepth.DETAILED.value,
        "description": "Level of detail for market analysis"
    },
    "market_type": {
        "type": "enum",
        "options": [e.value for e in MarketType],
        "default": MarketType.STOCKS.value,
        "description": "Type of financial market to analyze"
    },
    "analysis_method": {
        "type": "enum",
        "options": [e.value for e in AnalysisMethod],
        "default": AnalysisMethod.MIXED.value,
        "description": "Preferred analysis methodology"
    },
    "communication_style": {
        "type": "enum",
        "options": [e.value for e in CommunicationStyle],
        "default": CommunicationStyle.PROFESSIONAL.value,
        "description": "Preferred communication tone and style"
    },
    "language_complexity": {
        "type": "enum",
        "options": [e.value for e in LanguageComplexity],
        "default": LanguageComplexity.INTERMEDIATE.value,
        "description": "Technical language complexity level"
    },
    "enable_disclaimers": {
        "type": "boolean",
        "default": True,
        "description": "Whether to include legal disclaimers in responses"
    },
    "require_user_confirmation": {
        "type": "boolean",
        "default": True,
        "description": "Whether to ask for user confirmation at each step"
    },
    "output_format": {
        "type": "string",
        "options": ["markdown", "text", "json", "html", "csv"],
        "default": "markdown",
        "description": "Format for detailed output display"
    },
    "max_recommendations": {
        "type": "integer",
        "min": 1,
        "max": 20,
        "default": 5,
        "description": "Maximum number of strategy recommendations to provide"
    },
    "include_risk_warnings": {
        "type": "boolean",
        "default": True,
        "description": "Whether to include risk warnings in analysis"
    },
    "enable_step_by_step": {
        "type": "boolean",
        "default": True,
        "description": "Whether to use structured step-by-step process"
    },
    "show_confidence_scores": {
        "type": "boolean",
        "default": False,
        "description": "Display confidence scores for recommendations"
    },
    "include_sources": {
        "type": "boolean",
        "default": True,
        "description": "Include data sources and references"
    },
    "enable_backtesting": {
        "type": "boolean",
        "default": False,
        "description": "Enable historical performance backtesting"
    },
    "show_performance_metrics": {
        "type": "boolean",
        "default": True,
        "description": "Display performance metrics and KPIs"
    },
    "include_tax_implications": {
        "type": "boolean",
        "default": False,
        "description": "Include tax considerations in analysis"
    },
    "currency": {
        "type": "string",
        "options": ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "HKD", "SGD"],
        "default": "USD",
        "description": "Base currency for calculations"
    },
    "timezone": {
        "type": "string",
        "options": ["EST", "PST", "CST", "MST", "UTC", "GMT", "CET", "JST", "AEDT"],
        "default": "EST",
        "description": "Time zone for market hours and updates"
    },
    "update_frequency": {
        "type": "string",
        "options": ["real-time", "1-minute", "5-minute", "15-minute", "hourly", "daily"],
        "default": "real-time",
        "description": "Frequency of data updates"
    },
    "portfolio_size_limit": {
        "type": "integer",
        "min": 1,
        "max": 100,
        "default": 10,
        "description": "Maximum number of positions in portfolio"
    },
    "min_trade_size": {
        "type": "number",
        "min": 1,
        "max": 1000000,
        "default": 100,
        "description": "Minimum trade size in base currency"
    },
    "max_position_size": {
        "type": "number",
        "min": 0.01,
        "max": 1.0,
        "default": 0.25,
        "description": "Maximum position size as percentage of portfolio"
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
    "enable_notifications": {
        "type": "boolean",
        "default": False,
        "description": "Enable alert notifications"
    },
    "save_history": {
        "type": "boolean",
        "default": True,
        "description": "Save analysis and recommendation history"
    },
    "export_format": {
        "type": "string",
        "options": ["pdf", "excel", "csv", "json", "html"],
        "default": "pdf",
        "description": "Default export format for reports"
    },
    # Test-friendly configuration options
    "response_mode": {
        "type": "enum",
        "options": [e.value for e in ResponseMode],
        "default": ResponseMode.STANDARD.value,
        "description": "Response generation mode - deterministic for testing"
    },
    "introduction_style": {
        "type": "enum",
        "options": [e.value for e in IntroductionStyle],
        "default": IntroductionStyle.FULL.value,
        "description": "Style of initial introduction message"
    },
    "use_exact_phrases": {
        "type": "boolean",
        "default": False,
        "description": "Use exact predefined phrases for consistency"
    },
    "randomize_greetings": {
        "type": "boolean",
        "default": True,
        "description": "Allow variation in greeting messages"
    },
    "include_timestamp": {
        "type": "boolean",
        "default": False,
        "description": "Include timestamps in responses"
    },
    "use_numbered_steps": {
        "type": "boolean",
        "default": True,
        "description": "Number the steps in the process"
    },
    "enforce_disclaimer_format": {
        "type": "boolean",
        "default": True,
        "description": "Strictly enforce disclaimer formatting"
    },
    "subagent_announcement_style": {
        "type": "string",
        "options": ["explicit", "implicit", "none"],
        "default": "explicit",
        "description": "How to announce subagent usage"
    },
    "state_validation_level": {
        "type": "string",
        "options": ["strict", "moderate", "lenient"],
        "default": "strict",
        "description": "Level of state validation between steps"
    },
    "error_handling_verbosity": {
        "type": "string",
        "options": ["minimal", "standard", "detailed"],
        "default": "standard",
        "description": "Verbosity of error messages"
    },
    "test_mode": {
        "type": "boolean",
        "default": False,
        "description": "Enable test mode for consistent responses"
    },
    "response_template_version": {
        "type": "string",
        "options": ["v1", "v2", "custom"],
        "default": "v1",
        "description": "Version of response templates to use"
    },
    "greeting_variations": {
        "type": "boolean",
        "default": True,
        "description": "Allow variations in greeting text"
    },
    "step_transition_phrases": {
        "type": "string",
        "options": ["standard", "varied", "minimal"],
        "default": "standard",
        "description": "Style of transitions between steps"
    },
    "markdown_formatting_style": {
        "type": "string",
        "options": ["github", "standard", "minimal"],
        "default": "github",
        "description": "Markdown formatting style"
    },
    "quote_style": {
        "type": "string",
        "options": ["smart", "straight", "none"],
        "default": "smart",
        "description": "Style of quotation marks"
    },
    "line_break_style": {
        "type": "string",
        "options": ["unix", "windows", "auto"],
        "default": "unix",
        "description": "Line break style in responses"
    },
    "max_response_length": {
        "type": "integer",
        "min": 100,
        "max": 10000,
        "default": 5000,
        "description": "Maximum response length in characters"
    },
    "min_response_length": {
        "type": "integer",
        "min": 10,
        "max": 1000,
        "default": 50,
        "description": "Minimum response length in characters"
    },
    "allow_emoji": {
        "type": "boolean",
        "default": False,
        "description": "Allow emoji in responses"
    },
    "punctuation_style": {
        "type": "string",
        "options": ["standard", "minimal", "formal"],
        "default": "standard",
        "description": "Punctuation usage style"
    },
    "capitalization_style": {
        "type": "string",
        "options": ["sentence", "title", "lower"],
        "default": "sentence",
        "description": "Text capitalization style"
    },
    "number_format": {
        "type": "string",
        "options": ["comma", "space", "none"],
        "default": "comma",
        "description": "Number formatting style"
    },
    "date_format": {
        "type": "string",
        "options": ["ISO", "US", "EU", "UK"],
        "default": "ISO",
        "description": "Date formatting style"
    },
    "enforce_grammar_check": {
        "type": "boolean",
        "default": True,
        "description": "Enforce grammar checking on responses"
    },
    "allow_abbreviations": {
        "type": "boolean",
        "default": True,
        "description": "Allow abbreviations in responses"
    },
    "technical_term_handling": {
        "type": "string",
        "options": ["explain_first_use", "always_explain", "assume_knowledge"],
        "default": "explain_first_use",
        "description": "How to handle technical terms"
    }
}

FINANCIAL_COORDINATOR_PROMPT = """
Role: Act as Cymbal Financial Advisor from Cymbal Investment Services.
Your primary goal is to provide comprehensive financial advice by guiding users through a structured, step-by-step process. You will work with users to analyze market tickers, develop effective trading strategies, define clear execution plans, and thoroughly evaluate overall risk.

Overall Instructions for Interaction:

At the beginning, you must ALWAYS include ALL FIVE required elements in this exact order:

(1) Introduction:
Greet the user and clearly identify yourself as "Cymbal Financial Advisor from Cymbal Investment Services." State your main objective: to provide comprehensive financial advice through a step-by-step process. Emphasize that you will work together on market ticker analysis, trading strategies, execution plans, and risk evaluation. For example:

"Hello! I'm the Cymbal Financial Advisor from Cymbal Investment Services, here to help you navigate the world of financial decision-making. My main goal is to provide you with comprehensive financial advice through a structured, step-by-step process. We'll work together to analyze market tickers, develop effective trading strategies, define clear execution plans, and thoroughly evaluate overall risk."

(2) Process Overview:
Explicitly explain that the financial advisory process consists of FOUR key steps:
- Analyzing market tickers
- Developing effective trading strategies
- Defining clear execution plans
- Thoroughly evaluating overall risk

(3) User Instruction:
ALWAYS include: "Remember that at each step you can always ask to 'show me the detailed result as markdown'."

(4) Readiness Check:
ALWAYS ask: "Ready to get started?"

(5) Disclaimer:
You MUST include this exact disclaimer immediately with no omissions, truncations, or paraphrasing. Your response is NOT complete without it:

"Important Disclaimer: For Educational and Informational Purposes Only.
The information and trading strategy outlines provided by this tool, including any analysis, commentary, or potential scenarios, are generated by an AI model and are for educational and informational purposes only. They do not constitute, and should not be interpreted as, financial advice, investment recommendations, endorsements, or offers to buy or sell any securities or other financial instruments. Google and its affiliates make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, or availability with respect to the information provided. Any reliance you place on such information is therefore strictly at your own risk. This is not an offer to buy or sell any security. Investment decisions should not be made based solely on the information provided here. Financial markets are subject to risks, and past performance is not indicative of future results. You should conduct your own thorough research and consult with a qualified independent financial advisor before making any investment decisions. By using this tool and reviewing these strategies, you acknowledge that you understand this disclaimer and agree that Google and its affiliates are not liable for any losses or damages arising from your use of or reliance on this information."

State Management and Subagent Handoffs:

- At EACH step, you MUST explicitly announce which subagent you are calling (e.g., "I'll be using our data_analyst subagent for this step.") and validate that all REQUIRED state keys from previous steps are included when passing data to the next subagent.
- When requesting user input (such as ticker symbol, risk attitude, investment horizon), explain WHY it is needed and how it will be used by the relevant subagent.
- Upon receiving results from any subagent, provide a clear summary of the output AND explicitly describe how this result informs or modifies the next step in the financial analysis workflow.

Step-by-step breakdown (strictly follow this pattern):

* Gather Market Data Analysis (data_analyst subagent)
  - Announce: "Let's start with Market Data Analysis. I'll be using our data_analyst subagent for this."
  - Prompt the user: "Please provide the market ticker symbol you wish to analyze (e.g., AAPL, GOOGL, MSFT)." Explain that the ticker is needed so the data_analyst subagent can retrieve and analyze pertinent market data.
  - Call the data_analyst subagent, passing ONLY the user-provided ticker as state.
  - After completion, explain the contents of the data analysis output and how it sets the foundation for further strategy planning.

* Develop Trading Strategies (trading_analyst subagent)
  - Announce: "Next, we'll develop trading strategies using the trading_analyst subagent."
  - Prompt the user for their preferred risk attitude (e.g., conservative, moderate, aggressive) and investment period (short-term, medium-term, long-term). Explain the significance of these inputs for tailoring strategies.
  - Call the trading_analyst subagent, passing:
    - `market_data_analysis_output` (from previous step)
    - user-selected risk attitude
    - user-selected investment period
  - After completion, explain any strategy output and its implications for execution planning. Remind users they can request the result as markdown.

* Define Optimal Execution Strategy (execution_analyst subagent)
  - Announce: "Now, let's define an optimal execution strategy using the execution_analyst subagent."
  - Confirm with the user if they have broker or order preferences, and clarify which details may influence execution.
  - Call the execution_analyst subagent, passing:
    - trading strategy output
    - market analysis
    - risk attitude
    - investment period
    - user execution preferences (if provided)
  - After completion, summarize the execution plan, how it connects to the previous strategy, and any actionable next steps.

* Evaluate Overall Risk Profile (risk_analyst subagent)
  - Announce: "Finally, I'll evaluate the overall risk profile using the risk_analyst subagent."
  - Provide the aggregated state so far:
    - market data analysis output
    - trading strategy output
    - execution plan output
    - risk attitude
    - investment period
  - Call the risk_analyst subagent using all accumulated information.
  - After completion, explain the risk report, call out any detected misalignment with user preferences, and highlight important risks or considerations for investing.

At EVERY stage, confirm the correct state is maintained and transferred, ensure clear transitions between steps, and always provide explanations for both input requests and subagent outputs in context of the overall advice process.
"""
