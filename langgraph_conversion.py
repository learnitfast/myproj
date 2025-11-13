import json
from langgraph.graph import StateGraph, END

# Load the metagraph JSON
with open("metagraph.json", "r") as f:
    schema = json.load(f)

nodes = schema.get("nodes", {})
relationships = schema.get("relationships", {})

# --- Define state ---
class GraphState(dict):
    pass

# --- Initialize LangGraph ---
graph = StateGraph(GraphState)

# --- Add nodes from JSON ---
for node_name, fields in nodes.items():
    def make_node_func(name, fields):
        def node_func(state):
            # This is a placeholder – here you could add real logic
            print(f"Processing node: {name}")
            return state
        return node_func

    graph.add_node(node_name, make_node_func(node_name, fields))

# --- Add edges (relationships) ---
for rel_name, rel in relationships.items():
    from_node = rel["from"]
    to_node = rel["to"]
    if from_node in nodes and to_node in nodes:
        graph.add_edge(from_node, to_node)

# --- Choose entrypoint ---
# Pick a sensible start node (e.g. "Flight"), or use the first node
start_node = list(nodes.keys())[0]
graph.set_entry_point(start_node)

# --- Compile graph ---
compiled = graph.compile()

# --- Example run ---
if __name__ == "__main__":
    initial_state = GraphState()
    result = compiled.invoke(initial_state)
    print("Final state:", result)