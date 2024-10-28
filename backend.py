from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection function
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="ankit",
            password="R1AX4To518TmPKVIxVcwgOdDg",
            database="proj",
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
        return conn
    except Error:
        return None

# Route to add a new patient
@app.route('/add_patient', methods=['POST'])
def add_patient():
    data = request.json
    conn = create_connection()
    if conn:
        query = """
        INSERT INTO Patient (Patient_ID, First_Name, Last_Name, Gender, Date_of_Birth, Contact_Number, Email, Address, Visit_ID, Medical_History)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor = conn.cursor()
            cursor.execute(query, (
                data['Patient_ID'], data['First_Name'], data['Last_Name'],
                data['Gender'], data['Date_of_Birth'], data['Contact_Number'],
                data['Email'], data['Address'], data['Visit_ID'], data['Medical_History']
            ))
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Patient added successfully!'})
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)})
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed.'})

# Route to fetch all patients
@app.route('/patients', methods=['GET'])
def get_patients():
    conn = create_connection()
    if conn:
        query = "SELECT * FROM Patient"
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        patients = []
        for row in rows:
            patients.append({
                'Patient_ID': row[0],
                'First_Name': row[1],
                'Last_Name': row[2],
                'Gender': row[3],
                'Date_of_Birth': row[4],
                'Contact_Number': row[5],
                'Email': row[6],
                'Address': row[7],
                'Visit_ID': row[8],
                'Medical_History': row[9]
            })
        return jsonify({'status': 'success', 'data': patients})
    return jsonify({'status': 'error', 'message': 'Database connection failed.'})

# Route to delete a patient
@app.route('/delete_patient', methods=['DELETE'])
def delete_patient():
    data = request.json
    patient_id = data['Patient_ID']
    conn = create_connection()
    if conn:
        query = "DELETE FROM Patient WHERE Patient_ID = %s"
        cursor = conn.cursor()
        cursor.execute(query, (patient_id,))
        conn.commit()
        return jsonify({'status': 'success', 'message': f'Patient with ID {patient_id} deleted successfully!'})
    return jsonify({'status': 'error', 'message': 'Database connection failed.'})

# Route to add a new doctor
@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    data = request.json
    conn = create_connection()
    if conn:
        query = """
        INSERT INTO Doctor (Doctor_ID, First_Name, Last_Name, Specialization, Contact_Number, Email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            cursor = conn.cursor()
            cursor.execute(query, (
                data['Doctor_ID'], data['First_Name'], data['Last_Name'],
                data['Specialization'], data['Contact_Number'], data['Email']
            ))
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Doctor added successfully!'})
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)})
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed.'})

# Route to fetch all doctors
@app.route('/doctors', methods=['GET'])
def get_doctors():
    conn = create_connection()
    if conn:
        query = "SELECT * FROM Doctor"
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        doctors = []
        for row in rows:
            doctors.append({
                'Doctor_ID': row[0],
                'First_Name': row[1],
                'Last_Name': row[2],
                'Specialization': row[3],
                'Contact_Number': row[4],
                'Email': row[5]
            })
        return jsonify({'status': 'success', 'data': doctors})
    return jsonify({'status': 'error', 'message': 'Database connection failed.'})

# Route to delete a doctor
@app.route('/delete_doctor', methods=['DELETE'])
def delete_doctor():
    data = request.json
    doctor_id = data['Doctor_ID']
    conn = create_connection()
    if conn:
        query = "DELETE FROM Doctor WHERE Doctor_ID = %s"
        cursor = conn.cursor()
        cursor.execute(query, (doctor_id,))
        conn.commit()
        return jsonify({'status': 'success', 'message': f'Doctor with ID {doctor_id} deleted successfully!'})
    return jsonify({'status': 'error', 'message': 'Database connection failed.'})

# Route to add a new visit
@app.route('/add_visit', methods=['POST'])
def add_visit():
    data = request.json
    conn = create_connection()
    if conn:
        query = """
        INSERT INTO Visit (Visit_ID, Patient_ID, Doctor_ID, Visit_Date, Visit_Details)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor = conn.cursor()
            cursor.execute(query, (
                data['Visit_ID'], data['Patient_ID'], data['Doctor_ID'],
                data['Visit_Date'], data['Visit_Details']
            ))
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Visit added successfully!'})
        except Error as e:
            return jsonify({'status': 'error', 'message': str(e)})
        finally:
            conn.close()
    return jsonify({'status': 'error', 'message': 'Database connection failed.'})

# Route to fetch all visits
@app.route('/visits', methods=['GET'])
def get_visits():
    conn = create_connection()
    if conn:
        query = "SELECT * FROM Visit"
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        visits = []
        for row in rows:
            visits.append({
                'Visit_ID': row[0],
                'Patient_ID': row[1],
                'Doctor_ID': row[2],
                'Visit_Date': row[3],
                'Visit_Details': row[4]
            })
        return jsonify({'status': 'success', 'data': visits})
    return jsonify({'status': 'error', 'message': 'Database connection failed.'})

# Route to delete a visit
@app.route('/delete_visit', methods=['DELETE'])
def delete_visit():
    data = request.json
    visit_id = data['Visit_ID']
    conn = create_connection()
    if conn:
        query = "DELETE FROM Visit WHERE Visit_ID = %s"
        cursor = conn.cursor()
        cursor.execute(query, (visit_id,))
        conn.commit()
        return jsonify({'status': 'success', 'message': f'Visit with ID {visit_id} deleted successfully!'})
    return jsonify({'status': 'error', 'message': 'Database connection failed.'})

if __name__ == '__main__':
    app.run(debug=True)

