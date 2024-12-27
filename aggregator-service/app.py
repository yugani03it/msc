import os
import requests
import psycopg2
from flask import Flask, jsonify
from datetime import datetime


# Test update 

app = Flask(__name__)
#test Comment
# Load configurations from environment variables 
PATIENT_RECORD_URL = os.getenv('PATIENT_SERVICE_URL')
APPOINTMENT_URL = os.getenv('APPOINTMENT_SERVICE_URL')

DB_CONFIG = {   
    "host": os.getenv('DB_HOST'),
    "port": 5439,
    "dbname": os.getenv('DB_NAME'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD')
}

def fetch_patient_data():
    try:
        response = requests.get(f"{PATIENT_RECORD_URL}/patients")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching patient data: {e}")
        return []

def fetch_appointment_data():
    try:
        response = requests.get(f"{APPOINTMENT_URL}/appointments")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching appointment data: {e}")
        return []

def store_aggregated_data(data):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aggregated_data (
                id SERIAL PRIMARY KEY,
                total_patients INT,
                total_appointments INT,
                timestamp TIMESTAMP
            );
        """)

        # Insert aggregated data
        cursor.execute("""
            INSERT INTO aggregated_data (total_patients, total_appointments, timestamp)
            VALUES (%s, %s, %s);
        """, (data["total_patients"], data["total_appointments"], datetime.now()))

        conn.commit()
        cursor.close()
        conn.close()
        print("Aggregated data stored successfully.")
    except Exception as e:
        print(f"Error storing aggregated data: {e}")

@app.route('/aggregate', methods=['GET'])
def aggregate_data():
    patient_data = fetch_patient_data()
    appointment_data = fetch_appointment_data()

    aggregated_data = {
        "total_patients": len(patient_data),
        "total_appointments": len(appointment_data)
    }

    # Store data in Redshift
    store_aggregated_data(aggregated_data)

    return jsonify({"message": "Data aggregated successfully", "data": aggregated_data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)
