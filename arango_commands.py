from arango import ArangoClient

client = ArangoClient(hosts="http://localhost:8529")
db = client.db('testDB', username='root', password='mysecretpassword')


for name in ["Aircraft", "Flight", "Airport", "CrewMember", "MaintenanceEvent", "Passenger", "Booking"]:
    if not db.has_collection(name):
        db.create_collection(name)

if not db.has_collection("Relations"):
    db.create_collection("Relations", edge=True)
edge_collection = "Relations"
edge_definitions=[
    {"edge_collection":"Relations", "from_vertex_collections": ["Aircraft","Flight","CrewMember","Passenger","Booking"], "to_vertex_collections": ["Flight","Airport","MaintenanceEvent","Booking"], "assignmentTime": "2025-09-01T12:00:00Z"}]

nodes = {
    "Aircraft": [
        {"_key": "N123AB", "model": "B737-800", "tailNumber": "N123AB", "manufacturerSerialNumber": "MSN9876",
         "status": "In Service", "lastMaintenanceDate": "2025-06-01", "maxSeating": 162},
        {"_key": "N456CD", "model": "A320-200", "tailNumber": "N456CD", "manufacturerSerialNumber": "MSN6543",
         "status": "Maintenance", "lastMaintenanceDate": "2025-08-20", "maxSeating": 180}
    ],
    "Flight": [
        {"_key": "BAW123", "flightNumber": "BA123", "scheduledDeparture": "2025-09-03T08:30:00Z",
         "scheduledArrival": "2025-09-03T11:45:00Z", "status": "Scheduled", "aircraftId": "N123AB",
         "originAirport": "LHR", "destinationAirport": "JFK"},
        {"_key": "AF456", "flightNumber": "AF456", "scheduledDeparture": "2025-09-04T09:10:00Z",
         "scheduledArrival": "2025-09-04T12:40:00Z", "status": "Scheduled", "aircraftId": "N456CD",
         "originAirport": "CDG", "destinationAirport": "LHR"}
    ],
    "Airport": [
        {"_key": "LHR", "name": "London Heathrow", "city": "London", "country": "UK",
         "latitude": 51.47, "longitude": -0.4543, "timezone": "Europe/London"},
        {"_key": "JFK", "name": "John F. Kennedy Intl", "city": "New York", "country": "USA",
         "latitude": 40.6413, "longitude": -73.7781, "timezone": "America/New_York"},
        {"_key": "CDG", "name": "Charles de Gaulle", "city": "Paris", "country": "France",
         "latitude": 49.0097, "longitude": 2.5479, "timezone": "Europe/Paris"}
    ],
    "CrewMember": [
        {"_key": "CM001", "name": "Alice Taylor", "role": "Captain", "licenseNumber": "PL-2023-001", "baseAirport": "LHR"},
        {"_key": "CM002", "name": "Bob Johnson", "role": "First Officer", "licenseNumber": "PL-2023-002", "baseAirport": "CDG"}
    ],
    "MaintenanceEvent": [
        {"_key": "ME1001", "aircraftId": "N123AB", "type": "A-Check", "reportedAt": "2025-08-31T14:10:00Z",
         "completedAt": "2025-09-01T09:00:00Z", "notes": "Replaced hydraulic pump #2."}
    ],
    "Passenger": [
        {"_key": "P001", "name": "John Smith", "frequentFlyerNo": "BAFF12345", "nationality": "USA"},
        {"_key": "P002", "name": "Marie Curie", "frequentFlyerNo": "AF9999", "nationality": "France"},
        {"_key": "P003", "name": "David Beckham", "frequentFlyerNo": "None", "nationality": "UK"}
    ],
    "Booking": [
        {"_key": "BK001", "passengerId": "P001", "flightId": "BAW123", "seat": "14A",
         "bookingStatus": "Confirmed", "fareClass": "Economy"},
        {"_key": "BK002", "passengerId": "P002", "flightId": "AF456", "seat": "12C",
         "bookingStatus": "Checked-in", "fareClass": "Business"}
    ]
}

# ------------------------------
# 5. Insert Nodes
# ------------------------------
from langchain_community.graphs import ArangoGraph

graph = ArangoGraph(db)
if db.has_graph("aircraft_graph1"):
    db.delete_graph("aircraft_graph1", drop_collections=True)

db.create_graph(
    "aircraft_graph1",edge_definitions)

for collection_name, documents in nodes.items():
    collection = db.collection(collection_name)
    for doc in documents:
        if not collection.has(doc["_key"]):
            collection.insert(doc, overwrite=True)

# ------------------------------
# 6. Insert Edges
# ------------------------------
edges = [
    {"type": "OPERATES", "_from": "Aircraft/N123AB", "_to": "Flight/BAW123", "assignmentTime": "2025-09-01T12:00:00Z"},
    {"type": "OPERATES", "_from": "Aircraft/N456CD", "_to": "Flight/AF456", "assignmentTime": "2025-09-02T08:00:00Z"},
    {"type": "DEPARTS_FROM", "_from": "Flight/BAW123", "_to": "Airport/LHR", "gate": "A10"},
    {"type": "ARRIVES_AT", "_from": "Flight/BAW123", "_to": "Airport/JFK", "gate": "7"},
    {"type": "DEPARTS_FROM", "_from": "Flight/AF456", "_to": "Airport/CDG", "gate": "B5"},
    {"type": "ARRIVES_AT", "_from": "Flight/AF456", "_to": "Airport/LHR", "gate": "22"},
    {"type": "ASSIGNED_TO", "_from": "CrewMember/CM001", "_to": "Flight/BAW123", "role": "Captain", "assignedOn": "2025-09-01T15:00:00Z"},
    {"type": "ASSIGNED_TO", "_from": "CrewMember/CM002", "_to": "Flight/AF456", "role": "First Officer", "assignedOn": "2025-09-02T10:00:00Z"},
    {"type": "HAS_MAINTENANCE_EVENT", "_from": "Aircraft/N123AB", "_to": "MaintenanceEvent/ME1001", "severity": "Medium"},
    {"type": "HAS_BOOKING", "_from": "Passenger/P001", "_to": "Booking/BK001", "createdAt": "2025-08-20T12:00:00Z"},
    {"type": "HAS_BOOKING", "_from": "Passenger/P002", "_to": "Booking/BK002", "createdAt": "2025-08-22T14:30:00Z"},
    {"type": "FOR_FLIGHT", "_from": "Booking/BK001", "_to": "Flight/BAW123", "price": 450.0, "currency": "USD"},
    {"type": "FOR_FLIGHT", "_from": "Booking/BK002", "_to"      : "Flight/AF456", "price": 1200.0, "currency": "EUR"}
]
edge_col = db.collection(edge_collection)
for edge in edges:
    edge_col.insert(edge, overwrite=True)
