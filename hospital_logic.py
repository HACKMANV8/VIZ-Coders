import time
import random

# --- Database Simulation (In a real app, this would be SQLite, PostgreSQL, or MongoDB) ---

ROOM_SCHEDULE = {
    'Room 101': {'doctor': 'Dr. Smith', 'status': 'Occupied', 'next_free': '11:00 AM'},
    'Room 205': {'doctor': 'Dr. Patel', 'status': 'Occupied', 'next_free': '10:45 AM'},
    'Room 310': {'doctor': 'None', 'status': 'Available', 'next_free': 'N/A'},
    'Room 400': {'doctor': 'Dr. Lee', 'status': 'Cleaning Required', 'next_free': '11:30 AM'},
}

PHARMACY_INVENTORY = {
    'Paracetamol': {'stock': 450, 'available': 'Yes'},
    'Amoxicillin': {'stock': 120, 'available': 'Yes'},
    'Insulin Pens': {'stock': 5, 'available': 'Low Stock - Reorder Now'},
    'Lisinopril': {'stock': 0, 'available': 'No'},
}

# --- Core Functions for Staff ---

def get_room_availability():
    """Returns a list of all rooms and their current status."""
    print(f"\n--- ROOM AVAILABILITY ({time.strftime('%H:%M:%S')}) ---")
    available_rooms = 0
    for room, data in ROOM_SCHEDULE.items():
        print(f"Room: {room} | Status: {data['status']} | Doctor: {data['doctor']} | Next Free: {data['next_free']}")
        if data['status'] == 'Available':
            available_rooms += 1
    print(f"\nTotal Available Rooms: {available_rooms}")
    return available_rooms

def check_medication_stock(medication_name):
    """Checks the stock and availability of a specific medication."""
    med_name = medication_name.title() # Format input
    print(f"\n--- PHARMACY CHECK for {med_name} ---")
    if med_name in PHARMACY_INVENTORY:
        data = PHARMACY_INVENTORY[med_name]
        print(f"Stock Level: {data['stock']} units | Status: {data['available']}")
    else:
        print(f"Medication '{med_name}' not found in inventory.")

def manage_queue(patient_name, action='add'):
    """Simulates adding/removing a patient from the queue."""
    QUEUE = ['Alice', 'Bob', 'Charlie']
    
    if action == 'add':
        QUEUE.append(patient_name)
        print(f"\n{patient_name} added to queue. Current Queue: {', '.join(QUEUE)}")
    elif action == 'next' and QUEUE:
        next_patient = QUEUE.pop(0)
        print(f"\n{next_patient} is now being served (Token issued). Remaining Queue: {', '.join(QUEUE)}")
        return next_patient
    else:
        print("\nQueue is empty.")

# --- Execution Simulation ---

if __name__ == "__main__":
    print("Hospital Operations Backend Simulator Started.")
    
    # 1. Staff checks room availability
    get_room_availability()
    
    # 2. Staff checks pharmacy stock
    check_medication_stock("insulin pens")
    check_medication_stock("Lisinopril")
    
    # 3. Staff manages the queue
    manage_queue("Eve", 'add')
    manage_queue("Eve", 'next')