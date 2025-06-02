from dotenv import load_dotenv
from langchain_tavily import TavilySearch
import re

load_dotenv()

# =============================================================================
# SEARCH SETUP
# =============================================================================

web_search = TavilySearch(max_results=3)

# =============================================================================
# BULL AGENT TOOLS (Optimistic/Buy-focused)
# =============================================================================


def find_positive_news(stock_symbol: str):
    """Search for positive news and developments about a stock"""
    query = f"{stock_symbol} stock positive news earnings growth revenue profit upgrade"
    results = web_search.invoke(query)

    # Extract key positive points
    positive_signals = []
    for result in results:
        content = result.get("content", "")
        if any(
            word in content.lower()
            for word in [
                "profit",
                "growth",
                "upgrade",
                "beat",
                "strong",
                "positive",
                "bullish",
            ]
        ):
            positive_signals.append(
                f"• {result.get('title', 'News')}: {content[:200]}..."
            )

    if positive_signals:
        return f"🐂 POSITIVE SIGNALS for {stock_symbol}:\n" + "\n".join(
            positive_signals[:2]
        )
    else:
        return f"🐂 {stock_symbol}: Limited positive news found, but that could mean it's undervalued!"


def calculate_growth_potential(stock_symbol: str):
    """Calculate basic growth metrics and bullish indicators"""
    # Search for financial metrics
    query = f"{stock_symbol} stock price earnings revenue growth rate market cap"
    results = web_search.invoke(query)

    # Extract numbers and metrics (simplified)
    growth_indicators = []
    for result in results:
        content = result.get("content", "").lower()

        # Look for growth percentages
        percentages = re.findall(r"(\d+(?:\.\d+)?)\s*%", content)
        if percentages:
            growth_indicators.extend([f"{p}%" for p in percentages[:3]])

        # Look for positive growth terms
        if any(
            term in content
            for term in ["increase", "growth", "up", "higher", "rose", "gained"]
        ):
            growth_indicators.append("Positive trend detected")

    if growth_indicators:
        return f"📈 GROWTH POTENTIAL for {stock_symbol}: {', '.join(growth_indicators[:3])}"
    else:
        return f"📈 {stock_symbol}: Growth data limited, but could indicate overlooked opportunity!"


# =============================================================================
# BEAR AGENT TOOLS (Pessimistic/Sell-focused)
# =============================================================================


def find_negative_news(stock_symbol: str):
    """Search for negative news and risks about a stock"""
    query = f"{stock_symbol} stock negative news risks decline losses downgrade warning"
    results = web_search.invoke(query)

    # Extract key negative points
    negative_signals = []
    for result in results:
        content = result.get("content", "")
        if any(
            word in content.lower()
            for word in [
                "loss",
                "decline",
                "risk",
                "warning",
                "downgrade",
                "weak",
                "negative",
                "bearish",
                "concern",
            ]
        ):
            negative_signals.append(
                f"• {result.get('title', 'News')}: {content[:200]}..."
            )

    if negative_signals:
        return f"🐻 WARNING SIGNALS for {stock_symbol}:\n" + "\n".join(
            negative_signals[:2]
        )
    else:
        return f"🐻 {stock_symbol}: No major red flags found, but market volatility always poses risks!"


def assess_market_risks(stock_symbol: str):
    """Assess overall market risks and bearish indicators"""
    query = f"{stock_symbol} stock market risks volatility debt competition regulatory concerns"
    results = web_search.invoke(query)

    # Look for risk factors
    risk_factors = []
    for result in results:
        content = result.get("content", "").lower()

        # Look for risk terms
        if any(
            term in content
            for term in [
                "risk",
                "volatile",
                "uncertain",
                "concern",
                "debt",
                "competition",
            ]
        ):
            risk_factors.append("Market risk identified")

        # Look for negative percentages
        negative_changes = re.findall(r"down\s+(\d+(?:\.\d+)?)\s*%", content)
        if negative_changes:
            risk_factors.extend([f"Down {p}%" for p in negative_changes[:2]])

    if risk_factors:
        return f"⚠️ RISK ASSESSMENT for {stock_symbol}: {', '.join(risk_factors[:3])}"
    else:
        return f"⚠️ {stock_symbol}: Risk factors unclear - proceed with extreme caution!"


# =============================================================================
# CHAIRMAN AGENT TOOLS (Decision maker)
# =============================================================================


def get_current_market_sentiment(stock_symbol: str):
    """Get overall market sentiment and recent performance"""
    query = f"{stock_symbol} stock current price today market sentiment analyst rating"
    results = web_search.invoke(query)

    sentiment_data = []
    for result in results:
        content = result.get("content", "")
        title = result.get("title", "")

        # Look for current price info
        if any(
            word in (title + content).lower()
            for word in ["price", "trading", "market", "analyst"]
        ):
            sentiment_data.append(f"• {title}: {content[:150]}...")

    if sentiment_data:
        return f"📊 CURRENT MARKET DATA for {stock_symbol}:\n" + "\n".join(
            sentiment_data[:2]
        )
    else:
        return f"📊 {stock_symbol}: Market data limited - need more information for decision"


def make_investment_decision(stock_symbol: str, bull_points: str, bear_points: str):
    """Make final investment recommendation based on bull and bear arguments"""
    # Simple scoring based on argument strength
    bull_score = len(bull_points.split("•")) if "•" in bull_points else 1
    bear_score = len(bear_points.split("•")) if "•" in bear_points else 1

    # Look for strong signals in the arguments
    strong_bull_signals = any(
        word in bull_points.lower()
        for word in ["growth", "profit", "upgrade", "strong"]
    )
    strong_bear_signals = any(
        word in bear_points.lower()
        for word in ["risk", "decline", "warning", "concern"]
    )

    if bull_score > bear_score and strong_bull_signals:
        recommendation = "BUY"
        confidence = "High"
    elif bear_score > bull_score and strong_bear_signals:
        recommendation = "SELL/AVOID"
        confidence = "High"
    else:
        recommendation = "HOLD/RESEARCH MORE"
        confidence = "Medium"

    return (
        f"🎯 FINAL DECISION for {stock_symbol}: {recommendation}\n"
        f"Confidence Level: {confidence}\n"
        f"Bull Arguments: {bull_score} points\n"
        f"Bear Arguments: {bear_score} points\n"
        f"Recommendation: Based on current analysis, {recommendation.lower()} position"
    )
