# This is a sample Python script.
from langchain.llms import Ollama
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.schema import SystemMessage
from langchain.chains import LLMChain
from langchain.tools import Tool
import yfinance as yf
from langchain.agents import initialize_agent, AgentType
from langchain.agents import tool, initialize_agent, AgentExecutor, AgentType
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain.chains import LLMChain

llm = Ollama(model="llama2")
def get_stock_info(symbol: str) -> str:
    stock = yf.Ticker(symbol)
    info = stock.info
    return (
        f"{symbol}:\n"
        f"  Price: {info.get('regularMarketPrice', 'N/A')}\n"
        f"  Sector: {info.get('sector', 'N/A')}\n"
        f"  Market Cap: {info.get('marketCap', 'N/A')}\n"
        f"  Beta: {info.get('beta', 'N/A')}\n"
    )

market_analyst_prompt = PromptTemplate(
    template="""
You are a Market Analyst. Use the following tool to fetch data and summarize:
{input}
""",
    input_variables=["input"],
)
market_analyst_chain = LLMChain(llm=llm, prompt=market_analyst_prompt)

risk_analyst_prompt = PromptTemplate(
    template="""
You are a Risk Analyst. Evaluate the following stock data for volatility and risk:
{input}
""",
    input_variables=["input"],
)
risk_analyst_chain = LLMChain(llm=llm, prompt=risk_analyst_prompt)

portfolio_manager_prompt = PromptTemplate(
    template="""
You are a Portfolio Manager. Based on the following risk analysis, suggest 2 best medium-term investments:
{input}
""",
    input_variables=["input"],
)
portfolio_manager_chain = LLMChain(llm=llm, prompt=portfolio_manager_prompt)


@tool
def fetch_market_data(input: str) -> str:
    """Fetch market data for a comma-separated list of stock symbols."""
    symbols = [s.strip().upper() for s in input.split(",")]
    return "\n".join([get_stock_info(sym) for sym in symbols])
@tool
def multi_agent_pipeline(stock_symbols: str):
    # Step 1: Market Analyst gets data
    market_data = fetch_market_data.run(stock_symbols)
    market_summary = market_analyst_chain.run(input=market_data)

    # Step 2: Risk Analyst evaluates risk
    risk_analysis = risk_analyst_chain.run(input=market_summary)

    # Step 3: Portfolio Manager recommends
    recommendation = portfolio_manager_chain.run(input=risk_analysis)

    return {
        "market_summary": market_summary,
        "risk_analysis": risk_analysis,
        "recommendation": recommendation
    }


if __name__ == '__main__':
    # Step 3: Register tools
    stocks = "AAPL, MSFT, NVDA"
    result = multi_agent_pipeline(stocks)

    print("\n📊 Market Summary:\n", result["market_summary"])
    print("\n⚠️ Risk Analysis:\n", result["risk_analysis"])
    print("\n📈 Final Recommendation:\n", result["recommendation"])
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
