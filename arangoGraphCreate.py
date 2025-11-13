# Instantiate the ArangoDB-LangChain Graph
# Instantiate ArangoDB Database
import json

#from adb_cloud_connector import get_temp_credentials
from arango import ArangoClient

#con = get_temp_credentials()

db = ArangoClient(hosts="http://localhost:8529").db(
    "testDB", "root", "mysecretpassword", verify=True
)


from langchain_community.graphs import ArangoGraph

graph = ArangoGraph(db)
if db.has_graph("GameOfThrones"):
    db.delete_graph("GameOfThrones", drop_collections=True)

db.create_graph(
    "GameOfThrones",
    edge_definitions=[
        {
            "edge_collection": "ChildOf",
            "from_vertex_collections": ["Characters"],
            "to_vertex_collections": ["Characters"],
        },
    ],
)

documents = [
    {
        "_key": "NedStark",
        "name": "Ned",
        "surname": "Stark",
        "alive": True,
        "age": 41,
        "gender": "male",
    },
    {
        "_key": "CatelynStark",
        "name": "Catelyn",
        "surname": "Stark",
        "alive": False,
        "age": 40,
        "gender": "female",
    },
    {
        "_key": "AryaStark",
        "name": "Arya",
        "surname": "Stark",
        "alive": True,
        "age": 11,
        "gender": "female",
    },
    {
        "_key": "BranStark",
        "name": "Bran",
        "surname": "Stark",
        "alive": True,
        "age": 10,
        "gender": "male",
    },
]

edges = [
    {"_to": "Characters/NedStark", "_from": "Characters/AryaStark"},
    {"_to": "Characters/NedStark", "_from": "Characters/BranStark"},
    {"_to": "Characters/CatelynStark", "_from": "Characters/AryaStark"},
    {"_to": "Characters/CatelynStark", "_from": "Characters/BranStark"},
]

db.collection("Characters").import_bulk(documents)
db.collection("ChildOf").import_bulk(edges)