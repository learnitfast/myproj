import json
import sample_data
from langgraph.graph import StateGraph
class LangGraphQueryEngine:
    def __init__(self, compiled_graph, nodes, edges):
        self.graph = compiled_graph
        self.nodes = nodes
        self.edges = edges

    def match(self, from_type=None, rel_type=None, to_type=None, to_filter=None):
        """
        Query the instance graph stored in LangGraph.
        from_type, rel_type, to_type = strings matching node/edge labels
        to_filter = dict for filtering target node
        """
        results = []
        for edge in self.edges:
            if rel_type and edge["type"] != rel_type:
                continue

            from_node = next((n for t, lst in self.nodes.items() for n in lst if n["id"] == edge["from"]), None)
            to_node = next((n for t, lst in self.nodes.items() for n in lst if n["id"] == edge["to"]), None)

            if not from_node or not to_node:
                continue
            if from_type and from_node["id"][0] != from_type[0]:  # crude type check
                continue
            if to_type and to_node["id"][0] != to_type[0]:
                continue

            # filter target node
            if to_filter:
                ok = True
                for k, v in to_filter.items():
                    if str(to_node.get(k)) != str(v):
                        ok = False
                if not ok:
                    continue

            results.append((from_node, edge, to_node))

        return results

class InstanceState(dict):
    pass

instance_graph = StateGraph(InstanceState)


sample_nodes=sample_data.nodes
#print(sample_nodes)
sample_edges=sample_data.edges
# Add nodes dynamically from instance data
for node_type, node_list in sample_nodes.items():
    for node in node_list:
        node_id = node["id"]

        def make_node_func(nid, data):
            def node_func(state):
                state[nid] = data
                return state
            return node_func

        instance_graph.add_node(node_id, make_node_func(node_id, node))

# Add edges
for edge in sample_edges:
    instance_graph.add_edge(edge["from"], edge["to"])

# Pick entrypoint (say, a passenger)
instance_graph.set_entry_point("P001")

compiled_instance = instance_graph.compile()

if __name__ == "__main__":
    result = compiled_instance.invoke(InstanceState())
    print(result)
    #print("Final State:", result)
    print("Starting")
    engine = LangGraphQueryEngine(compiled_instance, sample_nodes, sample_edges)

    # 1. Flights departing from LHR
    res1 = engine.match(from_type="Flight", rel_type="DEPARTS_FROM", to_type="Airport", to_filter={"id": "LHR"})
    print(res1)
    for flight, edge, airport in res1:
        print(f"Flight {flight['id']} departs from {airport['name']}")

    # 2. Passengers booked on BAW123
    res2 = engine.match(from_type="Booking", rel_type="FOR_FLIGHT", to_type="Flight", to_filter={"id": "BAW123"})
    for booking, edge, flight in res2:
        passenger_edge = next(e for e in sample_edges if e["type"] == "HAS_BOOKING" and e["to"] == booking["id"])
        passenger = next(p for p in sample_nodes["Passenger"] if p["id"] == passenger_edge["from"])
        print(f"Passenger {passenger['name']} booked on {flight['id']}")
