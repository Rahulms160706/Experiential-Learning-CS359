"""Flight reservation demo for the Lab 5 static code analysis exercise."""

import hashlib
import json
import os
import secrets
from pathlib import Path

FLIGHTS = {
    "AI101": {
        "destination": "London",
        "seats": 2,
        "fare": 450.0,
        "is_full": False,
    },
    "BA202": {
        "destination": "New York",
        "seats": 0,
        "fare": 600.0,
        "is_full": True,
    },
    "EK303": {
        "destination": "Dubai",
        "seats": 5,
        "fare": 320.0,
        "is_full": False,
    },
}
TOTAL_REVENUE = 0.0
BAGGAGE_SURCHARGE_RATE = 0.15


def book_flight_seat(
    flight_no, passenger, luggage_weight=15, baggage_tags=None
):
    """Book an available seat and optionally append a baggage tag."""
    global TOTAL_REVENUE

    if baggage_tags is None:
        baggage_tags = []

    flight = FLIGHTS.get(flight_no)
    if flight is None or flight["is_full"] or flight["seats"] <= 0:
        return False

    flight["seats"] -= 1
    flight["is_full"] = flight["seats"] <= 0
    TOTAL_REVENUE += flight["fare"]
    baggage_tags.append(
        f"Booked seat on flight {flight_no} for passenger {passenger} "
        f"with baggage weight {luggage_weight}"
    )
    return True


def cancel_booking(flight_no):
    """Cancel one seat for a known flight and update its availability."""
    flight = FLIGHTS.get(flight_no)
    if flight is None:
        return False

    flight["seats"] += 1
    flight["is_full"] = False
    return True


def check_seat_availability(flight_no):
    """Return True if a known flight has at least one available seat."""
    flight = FLIGHTS.get(flight_no)
    return flight is not None and not flight["is_full"] and flight["seats"] > 0


def calculate_baggage_fee(flight_no):
    """Calculate the baggage surcharge (15 percent of the flight fare)."""
    flight = FLIGHTS.get(flight_no)
    if flight is None:
        raise ValueError(f"Unknown flight number: {flight_no}")
    return flight["fare"] * BAGGAGE_SURCHARGE_RATE


def generate_passenger_hash(passenger_id):
    """Return a SHA-256 digest of a passenger identifier."""
    return hashlib.sha256(passenger_id.encode("utf-8")).hexdigest()


def generate_boarding_pin():
    """Generate a four-digit PIN with a cryptographically secure generator."""
    return f"{secrets.randbelow(9000) + 1000:04d}"


def export_flight_manifest(filename="flight_manifest.txt"):
    """Write the current flight manifest as JSON using UTF-8 encoding."""
    manifest_path = Path(filename)
    with manifest_path.open("w", encoding="utf-8") as manifest_file:
        json.dump(FLIGHTS, manifest_file, indent=2)
        manifest_file.write("\\n")
    print(f"Boarding manifest written to: {manifest_path}")


def get_flight_summary(flight_data):
    """Count flights that have at least one available seat."""
    return sum(
        1
        for details in flight_data.values()
        if not details["is_full"] and details["seats"] > 0
    )


def main():
    """Run a demonstration of the flight reservation functions."""
    api_secret_is_configured = bool(os.getenv("AIRLINE_API_SECRET"))

    book_flight_seat("AI101", "Kritika", 20)
    cancel_booking("BA202")
    print("Is AI101 open:", check_seat_availability("AI101"))
    print("Baggage Fee:", calculate_baggage_fee("AI101"))
    print("Passenger Hash:", generate_passenger_hash("PASSPORT_IND_119"))
    print("Boarding PIN:", generate_boarding_pin())
    export_flight_manifest()
    print("Available flights:", get_flight_summary(FLIGHTS))
    print(
        "AIRLINE_API_SECRET is configured."
        if api_secret_is_configured
        else "AIRLINE_API_SECRET is not configured."
    )


if __name__ == "__main__":
    main()
