from arango import ArangoClient

client = ArangoClient(hosts="http://localhost:8529")
db = client.db('testDB', username='root', password='mysecretpassword')

meta_collections=["Aircraft_meta", "Flight_meta", "Airport_meta", "CrewMember_meta", "MaintenanceEvent_meta", "Passenger_meta", "Booking_meta"]

for name in meta_collections:
    if not db.has_collection(name):
        db.create_collection(name)

if not db.has_collection("Relations_meta"):
    db.create_collection("Relations_meta", edge=True)
edge_collection = "Relations_meta"
edge_definitions=[
    {"edge_collection":"Relations_meta", "from_vertex_collections": ["Aircraft_meta","Flight_meta","CrewMember_meta","Passenger_meta","Booking_meta"], "to_vertex_collections": ["Flight_meta","Airport_meta","MaintenanceEvent_meta","Booking_meta"], "assignmentTime": "2025-09-01T12:00:00Z"}
]
nodes ={
    "Aircraft_meta": [{
      "_key": "aircraft01",
      "id": {
        "type": "string",
        "description": "Unique aircraft identifier.",
        "example": "N123AB"
      },
      "model": {
        "type": "string",
        "description": "Aircraft model.",
        "example": "B737-800"
      },
      "tailNumber": {
        "type": "string",
        "description": "Registration / tail number.",
        "example": "N123AB"
      },
      "manufacturerSerialNumber": {
        "type": "string",
        "description": "Manufacturer serial number (MSN).",
        "example": "MSN9876"
      },
      "status": {
        "type": "enum",
        "description": "Operational state.",
        "values": ["In Service", "Grounded", "Maintenance"],
        "example": "In Service"
      },
      "lastMaintenanceDate": {
        "type": "date",
        "description": "Date of last maintenance check.",
        "example": "2025-06-01"
      },
      "maxSeating": {
        "type": "integer",
        "description": "Maximum seating capacity.",
        "example": 162
      },
      "identifiers": {
        "type": "list",
        "description": "model",
        "id": ["B737-800","A320-200"]
      }
    }],
    "Flight": [{
      "_key": "flight01",
      "id": {
        "type": "string",
        "description": "Unique flight identifier.",
        "example": "BAW123"
      },
      "flightNumber": {
        "type": "string",
        "description": "Commercial flight number.",
        "example": "BA123"
      },
      "scheduledDeparture": {
        "type": "datetime",
        "description": "Planned departure timestamp.",
        "example": "2025-09-03T08:30:00Z"
      },
      "scheduledArrival": {
        "type": "datetime",
        "description": "Planned arrival timestamp.",
        "example": "2025-09-03T11:45:00Z"
      },
      "status": {
        "type": "enum",
        "description": "Flight status.",
        "values": ["Scheduled", "Boarding", "Departed", "Arrived", "Cancelled", "Diverted"],
        "example": "Scheduled"
      },
      "aircraftId": {
        "type": "string",
        "description": "Reference to Aircraft.id used.",
        "example": "N123AB"
      },
      "originAirport": {
        "type": "string",
        "description": "IATA code for origin.",
        "example": "LHR"
      },
      "destinationAirport": {
        "type": "string",
        "description": "IATA code for destination.",
        "example": "JFK"
      },
      "identifiers": {
        "type": "list",
        "description": "flightNumber",
        "id": ["BA123","AF456"]
      }
    }],
    "Airport_meta": [{
      "_key": "airport01",
      "id": {
        "type": "string",
        "description": "Airport identifier (IATA or custom).",
        "example": "LHR"
      },
      "name": {
        "type": "string",
        "description": "Full airport name.",
        "example": "London Heathrow"
      },
      "city": {
        "type": "string",
        "description": "City.",
        "example": "London"
      },
      "country": {
        "type": "string",
        "description": "Country.",
        "example": "United Kingdom"
      },
      "latitude": {
        "type": "float",
        "description": "Geographic latitude.",
        "example": 51.47
      },
      "longitude": {
        "type": "float",
        "description": "Geographic longitude.",
        "example": -0.4543
      },
      "timezone": {
        "type": "string",
        "description": "Timezone identifier.",
        "example": "Europe/London"
      },
      "identifiers": {
        "type": "list",
        "description": "name",
        "id": ["London Heathrow","John F. Kennedy Intl","harles de Gaulle"]
      }
    }],
    "CrewMember_meta": [{
      "_key": "crewmember01",
      "id": {
        "type": "string",
        "description": "Crew member identifier.",
        "example": "CM456"
      },
      "name": {
        "type": "string",
        "description": "Full name.",
        "example": "A. Taylor"
      },
      "role": {
        "type": "enum",
        "description": "Job role.",
        "values": ["Captain", "First Officer", "Flight Attendant", "Engineer"],
        "example": "Captain"
      },
      "licenseNumber": {
        "type": "string",
        "description": "Pilot/crew license.",
        "example": "PL-2023-001"
      },
      "baseAirport": {
        "type": "string",
        "description": "Reference to Airport.id for crew base.",
        "example": "LHR"
      },
      "identifiers": {
        "type": "list",
        "description": "name",
        "id": ["A. Taylor","Bob Johnson"]
      }
    }],
    "MaintenanceEvent_meta": [{
      "_key": "maint01",
      "id": {
        "type": "string",
        "description": "Unique event id.",
        "example": "ME1001"
      },
      "aircraftId": {
        "type": "string",
        "description": "Reference to Aircraft.id.",
        "example": "N123AB"
      },
      "type": {
        "type": "enum",
        "description": "Maintenance type.",
        "values": ["A-Check", "B-Check", "C-Check", "UnscheduledRepair"],
        "example": "A-Check"
      },
      "reportedAt": {
        "type": "datetime",
        "description": "Report timestamp.",
        "example": "2025-08-31T14:10:00Z"
      },
      "completedAt": {
        "type": "datetime|null",
        "description": "Completion timestamp or null if open.",
        "example": "2025-09-01T09:00:00Z"
      },
      "notes": {
        "type": "string",
        "description": "Free-form description.",
        "example": "Replaced hydraulic pump #2."
      },
      "identifiers": {
        "type": "list",
        "description": "id",
        "id": ["ME1001"]
      }
    }],
    "Passenger_meta": [{
      "_key": "passenger01",
      "id": {
        "type": "string",
        "description": "Passenger identifier.",
        "example": "P789"
      },
      "name": {
        "type": "string",
        "description": "Full name.",
        "example": "J. Smith"
      },
      "frequentFlyerNo": {
        "type": "string|null",
        "description": "Loyalty number.",
        "example": "BAFF12345"
      },
      "nationality": {
        "type": "string",
        "description": "Country.",
        "example": "United States"
      },
      "identifiers": {
        "type": "list",
        "description": "name",
        "id": ["John Smith","Marie Curie","David Beckham"]
      }
    }],
    "Booking": [{
      "_key": "booking01",
      "id": {
        "type": "string",
        "description": "Booking or reservation id.",
        "example": "BK20250903-001"
      },
      "passengerId": {
        "type": "string",
        "description": "Reference to Passenger.id.",
        "example": "P789"
      },
      "flightId": {
        "type": "string",
        "description": "Reference to Flight.id.",
        "example": "BAW123"
      },
      "seat": {
        "type": "string|null",
        "description": "Seat assignment.",
        "example": "14A"
      },
      "bookingStatus": {
        "type": "enum",
        "description": "Booking status.",
        "values": ["Confirmed", "Checked-in", "Cancelled", "No-show"],
        "example": "Confirmed"
      },
      "fareClass": {
        "type": "string",
        "description": "Cabin/fare class.",
        "example": "Economy"
      },
      "identifiers": {
        "type": "list",
        "description": "id",
        "id": ["BK001","BK002"]
      }
    }]
  }

# ------------------------------
# 5. Insert Nodes
# ------------------------------
from langchain_community.graphs import ArangoGraph

graph = ArangoGraph(db)
if db.has_graph("aircraft_graph_meta"):
    db.delete_graph("aircraft_graph_meta", drop_collections=True)

db.create_graph(
    "aircraft_graph_meta",edge_definitions)

for collection_name, documents in nodes.items():
    collection = db.collection(collection_name)
    for doc in documents:
        if not collection.has(doc["_key"]):
            collection.insert(doc, overwrite=True)

# ------------------------------
# 6. Insert Edges
# ------------------------------
edges = [
    {"type": "OPERATES", "_from": "Aircraft/aircraft01", "_to": "Flight/flight01", "assignmentTime": "2025-09-01T12:00:00Z"},
    {"type": "DEPARTS_FROM", "_from": "Flight/flight01", "_to": "Airport/airport01", "gate": "A10"},
    {"type": "ARRIVES_AT", "_from": "Flight/flight01", "_to": "Airport/airport01", "gate": "7"},
    {"type": "ASSIGNED_TO", "_from": "CrewMember/crewmember01", "_to": "Flight/flight01", "assignedOn": "2025-09-01T15:00:00Z"},
    {"type": "HAS_MAINTENANCE_EVENT", "_from": "Aircraft/aircraft01", "_to": "MaintenanceEvent/maint01", "severity": "Medium"},
    {"type": "HAS_BOOKING", "_from": "Passenger/passenger01", "_to": "Booking/booking01", "createdAt": "2025-08-20T12:00:00Z"},
    {"type": "FOR_FLIGHT", "_from": "Booking/booking01", "_to": "Flight/flight01", "price": 450.0, "currency": "USD"}
]
edge_col = db.collection(edge_collection)
for edge in edges:
    edge_col.insert(edge, overwrite=True)
