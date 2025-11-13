# This is a sample Python script.
from langchain.llms import Ollama
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.schema import SystemMessage
from langchain.chains import LLMChain
from langchain.tools import Tool
import yfinance as yf
from langchain.agents import initialize_agent, AgentType

def get_stock_info(symbol: str) -> str:
    stock = yf.Ticker(symbol)
    info = stock.info
    return f"{symbol}: Price: {info.get('regularMarketPrice', 'N/A')}, Sector: {info.get('sector', 'N/A')}"

stock_tool = Tool(
    name="Stock Info Tool",
    func=get_stock_info,
    description="Gets the current stock price and sector by ticker symbol"
)

from langchain.prompts import PromptTemplate

# Step 1: Setup the LLaMA2 model via Ollama
llm = Ollama(model="llama2")

# Step 2: Define agent tools as LangChain @tool functions
""" 
@tool
def research_tool(topic: str) -> str:
    #Performs in-depth research on a topic
    return f"Researching the topic: {topic}. [Simulated research results]"

@tool
def summarization_tool(text: str) -> str:
    #Summarizes given input text
    return f"Summary of: {text[:100]}..."

@tool
def code_generator(prompt: str) -> str:
    #Generates code based on the prompt
    return f"# Code generated for prompt: {prompt}\nprint('Hello, world!')"

"""

# Step 5: Run the multi-agent pipeline




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Step 3: Register tools
    """
    tools = [research_tool, summarization_tool, code_generator]

    # Step 4: Initialize the main agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    query = "Build a tool that suggest on stock tips, summarizes it, and outputs Python code for displaying summaries."
    response = agent.run(query)
    print("\n--- Final Response ---\n", response)
    """
    market_agent = initialize_agent(
        tools=[stock_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    # Step 1: Market Analyst gathers info
    stocks = ["AAPL", "MSFT", "NVDA"]
    market_summary = "\n".join([get_stock_info(symbol) for symbol in stocks])
    print(market_summary)
    # Step 2: Risk Analyst evaluates
    risk_query = f"Analyze the volatility and risk of the following stocks:\n{market_summary}"
    risk_assessment = llm.invoke(risk_query)

    # Step 3: Portfolio Manager recommends
    portfolio_query = f"Given this risk analysis:\n{risk_assessment}\n\nWhich 2 stocks are best to invest in for medium-term growth?"
    final_recommendation = llm.invoke(portfolio_query)

    print("📈 Final Stock Recommendation:\n")
    print(final_recommendation)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
