#!/usr/bin/env python3
"""
Investment Committee Multi-Agent System

A command-line interface for analyzing stock investments using a multi-agent system
with bull, bear, and chairman agents that debate and make investment decisions.
"""

import sys
from src.agents import create_investment_supervisor
from src.utils import pretty_print_messages


def print_welcome():
    """Print welcome message and system description"""
    print("💼 INVESTMENT COMMITTEE SYSTEM")
    print("=" * 50)
    print("🐂 Bull Agent: Finds reasons to BUY")
    print("🐻 Bear Agent: Finds reasons to AVOID")
    print("🎯 Chairman: Makes final decision")
    print("=" * 50)


def analyze_stock(supervisor, stock_symbol):
    """Analyze a stock using the investment committee"""
    print(f"\n📈 ANALYZING: {stock_symbol.upper()}")
    print("-" * 30)

    user_query = f"Should I invest in {stock_symbol} stock? I want to hear both bullish and bearish arguments before making a decision."

    for chunk in supervisor.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_query,
                }
            ]
        },
    ):
        pretty_print_messages(chunk, last_message=True)


def main():
    """Main application entry point"""
    print_welcome()

    # Create the investment supervisor
    print("🔄 Initializing investment committee...")
    supervisor = create_investment_supervisor()
    print("✅ Committee ready!\n")

    # Interactive mode
    while True:
        try:
            stock_input = input("Enter stock symbol (or 'quit' to exit): ").strip()

            if stock_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Goodbye! Happy investing!")
                break

            if not stock_input:
                print("Please enter a valid stock symbol.")
                continue

            analyze_stock(supervisor, stock_input)

            print("\n" + "=" * 50)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Happy investing!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again with a different stock symbol.")


if __name__ == "__main__":
    main()
