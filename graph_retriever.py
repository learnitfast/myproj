from langchain.chains import LLMChain
from langchain_community.llms.ollama import Ollama
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain.prompts import PromptTemplate
# LLM


# Your custom retriever (pseudo-code)
def graph_retriever(query, graph):
    """
    Given a query, return relevant nodes/edges as context.
    """
    # naive: match nodes by name or id
    context = []
    for node_type, node_list in graph["nodes"].items():
        for n in node_list:
            if query.lower() in str(n).lower():
                context.append((node_type, n))
    return context


def neo_graph_extractor():
    # 1. Connect to Neo4j
    graph = Neo4jGraph(
        url="bolt://localhost:7687",
        username="neo4j",
        password="Test#1234"
    )

    # 2. Initialize LLM (OpenAI recommended for Cypher gen)
    llm = Ollama(model="llama2", temperature=0)

    # 3. Create Graph RAG chain


    cypher_prompt = PromptTemplate.from_template(
        """You are an expert at generating Cypher queries for Neo4j.
        The user will ask a question in natural language.
        Generate only a valid Cypher query, nothing else.
        Also in case of error try adjusting the query
        Question: {question}
        Cypher:"""
    )

    chain = GraphCypherQAChain.from_llm(
        llm,
        graph=graph,
        cypher_prompt=cypher_prompt,
        verbose=True,
        allow_dangerous_requests=True
    )

    # 4. Run a natural language query
    result = chain.run("Can you retrieve all the nodes and relationships?")
    print("Answer:", result)

    return result

# Wrap into chain
def answer_with_graph(query, graph):
    context = graph_retriever(query, graph)
    context_text = "\n".join([f"{t}: {n}" for t,n in context])

    prompt = PromptTemplate.from_template("""
    You are a QA assistant. 
    Use the following graph context to answer the question.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """)

    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(context=context_text, question=query)

if __name__ == '__main__':
    neo_graph_extractor()
    