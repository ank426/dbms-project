from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "ankit",
    "password": "R1AX4To518TmPKVIxVcwgOdDg",
    "database": "proj",
    "charset": "utf8mb4",
    "collation": "utf8mb4_general_ci"
}

def create_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Helper function to convert MySQL datetime to string
def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

# Generic GET endpoint for any table
@app.route('/api/<table>', methods=['GET'])
def get_all(table):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM {table}")
            results = cursor.fetchall()
            return jsonify({
                'status': 'success',
                'data': json.loads(json.dumps(results, default=datetime_handler))
            })
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

# Patient endpoints
@app.route('/api/patients', methods=['POST'])
def add_patient():
    data = request.json
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO Patient (
              Patient_ID, First_Name, Last_Name, Age, Gender, Date_of_Birth, Contact_Number, Email, Address, Medical_History
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['Patient_ID'], data['First_Name'], data['Last_Name'], data['Age'],
                data['Gender'], data['Date_of_Birth'], data['Contact_Number'],
                data['Email'], data['Address'], data['Medical_History']
            ))
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Patient added successfully'})
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Patient WHERE Patient_ID = %s", (patient_id,))
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Patient deleted successfully'})
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

# Doctor endpoints
@app.route('/api/doctors', methods=['POST'])
def add_doctor():
    data = request.json
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO Doctor (Doctor_ID, First_Name, Last_Name, Specialization,
                              Contact_Number, Email, Lab_ID)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['Doctor_ID'], data['First_Name'], data['Last_Name'],
                data['Specialization'], data['Contact_Number'], data['Email'],
                data['Lab_ID']
            ))
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Doctor added successfully'})
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

@app.route('/api/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Doctor WHERE Doctor_ID = %s", (doctor_id,))
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Doctor deleted successfully'})
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

# Laboratory endpoints
@app.route('/api/laboratories', methods=['POST'])
def add_laboratory():
    data = request.json
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO Laboratory (Lab_ID, Name, Location, Contact_Number, Email)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['Lab_ID'], data['Name'], data['Location'],
                data['Contact_Number'], data['Email']
            ))
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Laboratory added successfully'})
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

# Visit endpoints
@app.route('/api/visits', methods=['POST'])
def add_visit():
    data = request.json
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO Visit (Visit_ID, Patient_ID, Doctor_ID, Visit_Date,
                             Visit_Details, Prescription_ID)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['Visit_ID'], data['Patient_ID'], data['Doctor_ID'],
                data['Visit_Date'], data['Visit_Details'], data.get('Prescription_ID')
            ))
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Visit added successfully'})
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

# Medication endpoints
@app.route('/api/medications', methods=['POST'])
def add_medication():
    data = request.json
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO Medication (Medication_ID, Name, Manufacturer_ID, Dosage,
                                  Side_Effects, Frequency, Administration_Method)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['Medication_ID'], data['Name'], data['Manufacturer_ID'],
                data['Dosage'], data['Side_Effects'], data['Frequency'],
                data['Administration_Method']
            ))
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Medication added successfully'})
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

# Clinical Trial endpoints
@app.route('/api/clinical_trials', methods=['POST'])
def add_clinical_trial():
    data = request.json
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO Clinical_Trial (Trial_ID, Trial_Name, Description,
                                      Trial_Start_Date, Trial_End_Date,
                                      Patient_ID, Medication_ID, Doctor_ID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['Trial_ID'], data['Trial_Name'], data['Description'],
                data['Trial_Start_Date'], data['Trial_End_Date'],
                data['Patient_ID'], data['Medication_ID'], data['Doctor_ID']
            ))
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Clinical Trial added successfully'})
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

# Results endpoints
@app.route('/api/results', methods=['POST'])
def add_result():
    data = request.json
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO Results (Result_ID, Trial_ID, Lab_ID, Patient_ID,
                               Result_Date, Result_Details)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['Result_ID'], data['Trial_ID'], data['Lab_ID'],
                data['Patient_ID'], data['Result_Date'], data['Result_Details']
            ))
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Result added successfully'})
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

# Reactions endpoints
@app.route('/api/reactions', methods=['POST'])
def add_reaction():
    data = request.json
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO Reactions (Reaction_ID, Patient_ID, Medication_ID,
                                 Reaction_Details, Date_of_Reaction)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['Reaction_ID'], data['Patient_ID'], data['Medication_ID'],
                data['Reaction_Details'], data['Date_of_Reaction']
            ))
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Reaction added successfully'})
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

# Generic delete endpoint for any table
@app.route('/api/<table>/<int:id>', methods=['DELETE'])
def delete_record(table, record_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Determine the ID column name based on the table
            id_columns = {
                'Patient': 'Patient_ID',
                'Doctor': 'Doctor_ID',
                'Laboratory': 'Lab_ID',
                'Visit': 'Visit_ID',
                'Medication': 'Medication_ID',
                'Clinical_Trial': 'Trial_ID',
                'Results': 'Result_ID',
                'Reactions': 'Reaction_ID'
            }
            id_column = id_columns.get(table)
            if not id_column:
                return jsonify({'status': 'error', 'message': 'Invalid table name'}), 400

            cursor.execute(f"DELETE FROM {table} WHERE {id_column} = %s", (record_id,))
            conn.commit()
            return jsonify({'status': 'success', 'message': f'{table} record deleted successfully'})
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

@app.route('/api/trial_information/<int:trial_id>', methods=['GET'])
def get_trial_information(trial_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('GetTrialInformation', [trial_id])
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            return jsonify({
                'status': 'success',
                'data': json.loads(json.dumps(results, default=datetime_handler))
            })
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
