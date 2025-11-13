from arango import ArangoClient
from langchain_arangodb.graphs import
from langchain_openai import ChatOpenAI
from langchain.chains import GraphQAChain

# --- 1️⃣ Connect to ArangoDB ---
client = ArangoClient()
db = client.db(
    "testDB",
    username="root",
    password="mysecretpassword"
)

# --- 2️⃣ Initialize LangChain Graph Wrapper ---
graph = ArangoGraph(db)

# --- 3️⃣ Define your LLM (ChatGPT / GPT-4) ---
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

# --- 4️⃣ Create a GraphQAChain ---
chain = GraphQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True
)

# --- 5️⃣ Ask questions in plain English ---
query = "Which passengers have booked flight BA123?"
result = chain.run(query)
print(result)