nodes = {
    "Aircraft": [
        {"id": "N123AB", "model": "B737-800", "tailNumber": "N123AB", "manufacturerSerialNumber": "MSN9876", "status": "In Service", "lastMaintenanceDate": "2025-06-01", "maxSeating": 162},
        {"id": "N456CD", "model": "A320-200", "tailNumber": "N456CD", "manufacturerSerialNumber": "MSN6543", "status": "Maintenance", "lastMaintenanceDate": "2025-08-20", "maxSeating": 180}
    ],
    "Flight": [
        {"id": "BAW123", "flightNumber": "BA123", "scheduledDeparture": "2025-09-03T08:30:00Z", "scheduledArrival": "2025-09-03T11:45:00Z", "status": "Scheduled", "aircraftId": "N123AB", "originAirport": "LHR", "destinationAirport": "JFK"},
        {"id": "AF456", "flightNumber": "AF456", "scheduledDeparture": "2025-09-04T09:10:00Z", "scheduledArrival": "2025-09-04T12:40:00Z", "status": "Scheduled", "aircraftId": "N456CD", "originAirport": "CDG", "destinationAirport": "LHR"}
    ],
    "Airport": [
        {"id": "LHR", "name": "London Heathrow", "city": "London", "country": "UK", "latitude": 51.47, "longitude": -0.4543, "timezone": "Europe/London"},
        {"id": "JFK", "name": "John F. Kennedy Intl", "city": "New York", "country": "USA", "latitude": 40.6413, "longitude": -73.7781, "timezone": "America/New_York"},
        {"id": "CDG", "name": "Charles de Gaulle", "city": "Paris", "country": "France", "latitude": 49.0097, "longitude": 2.5479, "timezone": "Europe/Paris"}
    ],
    "CrewMember": [
        {"id": "CM001", "name": "Alice Taylor", "role": "Captain", "licenseNumber": "PL-2023-001", "baseAirport": "LHR"},
        {"id": "CM002", "name": "Bob Johnson", "role": "First Officer", "licenseNumber": "PL-2023-002", "baseAirport": "CDG"}
    ],
    "MaintenanceEvent": [
        {"id": "ME1001", "aircraftId": "N123AB", "type": "A-Check", "reportedAt": "2025-08-31T14:10:00Z", "completedAt": "2025-09-01T09:00:00Z", "notes": "Replaced hydraulic pump #2."}
    ],
    "Passenger": [
        {"id": "P001", "name": "John Smith", "frequentFlyerNo": "BAFF12345", "nationality": "USA"},
        {"id": "P002", "name": "Marie Curie", "frequentFlyerNo": "AF9999", "nationality": "France"},
        {"id": "P003", "name": "David Beckham", "frequentFlyerNo": "None", "nationality": "UK"}
    ],
    "Booking": [
        {"id": "BK001", "passengerId": "P001", "flightId": "BAW123", "seat": "14A", "bookingStatus": "Confirmed", "fareClass": "Economy"},
        {"id": "BK002", "passengerId": "P002", "flightId": "AF456", "seat": "12C", "bookingStatus": "Checked-in", "fareClass": "Business"}
    ]
}

edges= [
    {"type": "OPERATES", "from": "N123AB", "to": "BAW123", "assignmentTime": "2025-09-01T12:00:00Z"},
    {"type": "OPERATES", "from": "N456CD", "to": "AF456", "assignmentTime": "2025-09-02T08:00:00Z"},
    {"type": "DEPARTS_FROM", "from": "BAW123", "to": "LHR", "gate": "A10"},
    {"type": "ARRIVES_AT", "from": "BAW123", "to": "JFK", "gate": "7"},
    {"type": "DEPARTS_FROM", "from": "AF456", "to": "CDG", "gate": "B5"},
    {"type": "ARRIVES_AT", "from": "AF456", "to": "LHR", "gate": "22"},
    {"type": "ASSIGNED_TO", "from": "CM001", "to": "BAW123", "role": "Captain", "assignedOn": "2025-09-01T15:00:00Z"},
    {"type": "ASSIGNED_TO", "from": "CM002", "to": "AF456", "role": "First Officer", "assignedOn": "2025-09-02T10:00:00Z"},
    {"type": "HAS_MAINTENANCE_EVENT", "from": "N123AB", "to": "ME1001", "severity": "Medium"},
    {"type": "HAS_BOOKING", "from": "P001", "to": "BK001", "createdAt": "2025-08-20T12:00:00Z"},
    {"type": "HAS_BOOKING", "from": "P002", "to": "BK002", "createdAt": "2025-08-22T14:30:00Z"},
    {"type": "FOR_FLIGHT", "from": "BK001", "to": "BAW123", "price": 450.0, "currency": "USD"},
    {"type": "FOR_FLIGHT", "from": "BK002", "to": "AF456", "price": 1200.0, "currency": "EUR"}
]