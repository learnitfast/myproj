import os

#from arango.database import StandardDatabase
#from arango import database
#from langchain_arangodb.graphs.arangodb_graph import get_arangodb_client, ArangoGraph
from langchain_community.graphs import ArangoGraph
from langchain.chains import ArangoGraphQAChain
from langchain_community.llms.ollama import Ollama
from langchain.schema import LLMResult
from openai import api_key


def get_deepseek_llm(model: str = "deepseek-chat", api_key: str = None):
    """
    if api_key is None:
        api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key is None:
        raise ValueError("Please set DEEPSEEK_API_KEY environment variable")
    # Initialize DeepSeek LLM wrapper
    """
    llm = Ollama(model=model, temperature=0)
    return llm


def main():
    # 1. Connect to ArangoDB
    url = "http://localhost:8529"
    username = "root"
    password = os.getenv("ARANGO_ROOT_PASSWORD", "mysecretpassword")
    dbname = "testDB"

    #client = ArangoClient(hosts=url)
    #db = client.db(dbname, username=username, password=password)

    # Alternatively using helper:
    #connection = get_arangodb_client(url=url, dbname=dbname, username=username, password=password)
    #db=StandardDatabase(connection)
    # 2. Wrap with ArangoGraph
    #graph = ArangoGraph(db)
    from arango import ArangoClient


    db = ArangoClient(hosts=url).db(
        dbname, username, password, verify=True
    )
    """
    graph = ArangoGraph.from_db_credentials(
        url=url,
        username=username,
        password=password,
        dbname=dbname
    )
    """
    graph = ArangoGraph(db)
    # 3. Initialize the LLM (DeepSeek)
    llm = get_deepseek_llm(model="deepseek-coder:6.7b",api_key=api_key)

    # 4. Set up a QA Chain
    chain = ArangoGraphQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=True,
        allow_dangerous_requests=True  # depending on your trust level
    )

    # 5. Run some natural-language queries
    questions = [
        "Which aircraft is assigned to flight BAW123?",
        "What is the status of aircraft N456CD?",
        "Who is the captain assigned to flight BAW123?"
    ]

    for q in questions:
        print(f"> Question: {q}")
        response = chain.run(q)
        print(f"Response: {response}\n")

    chain.run("Is Ned Stark alive?")
if __name__ == "__main__":
    api_key="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"
    main()
