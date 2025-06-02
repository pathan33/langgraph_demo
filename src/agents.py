from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model

from .config import (
    MODEL_NAME,
    BULL_AGENT_PROMPT,
    BEAR_AGENT_PROMPT,
    CHAIRMAN_AGENT_PROMPT,
    SUPERVISOR_PROMPT,
)
from .tools import (
    find_positive_news,
    calculate_growth_potential,
    find_negative_news,
    assess_market_risks,
    get_current_market_sentiment,
    make_investment_decision,
)

load_dotenv()

# =============================================================================
# AGENT CREATION
# =============================================================================


def create_bull_agent():
    """Create the bull (optimistic) investment agent"""
    return create_react_agent(
        model=MODEL_NAME,
        tools=[find_positive_news, calculate_growth_potential],
        prompt=BULL_AGENT_PROMPT,
        name="bull_agent",
    )


def create_bear_agent():
    """Create the bear (pessimistic) investment agent"""
    return create_react_agent(
        model=MODEL_NAME,
        tools=[find_negative_news, assess_market_risks],
        prompt=BEAR_AGENT_PROMPT,
        name="bear_agent",
    )


def create_chairman_agent():
    """Create the chairman (decision maker) agent"""
    return create_react_agent(
        model=MODEL_NAME,
        tools=[get_current_market_sentiment, make_investment_decision],
        prompt=CHAIRMAN_AGENT_PROMPT,
        name="chairman_agent",
    )


def create_investment_supervisor():
    """Create the supervisor that manages the investment committee"""
    bull_agent = create_bull_agent()
    bear_agent = create_bear_agent()
    chairman_agent = create_chairman_agent()

    supervisor = create_supervisor(
        model=init_chat_model(MODEL_NAME),
        agents=[bull_agent, bear_agent, chairman_agent],
        prompt=SUPERVISOR_PROMPT,
        add_handoff_back_messages=True,
        output_mode="full_history",
    ).compile()

    return supervisor
