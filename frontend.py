import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

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
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

def sidebar_nav():
    st.sidebar.title("Navigation")
    pages = ['Home', 'Patients', 'Doctors', 'Laboratories', 'Visits',
             'Medications', 'Manufacturers', 'Clinical Trials', 'Results', 'Reactions']
    st.session_state.current_page = st.sidebar.radio("Go to", pages)

def fetch_all(table_name):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        conn.close()
        return result
    return []

def delete_record(table_name, id_column, id_value):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = %s", (id_value,))
            conn.commit()
            st.success(f"Record deleted successfully from {table_name}")
        except Error as e:
            st.error(f"Error deleting record: {e}")
        finally:
            conn.close()

def update_record(table_name, id_column, record_id, update_dict):
    """
    Generic function to update a record in any table

    Args:
        table_name (str): Name of the table to update
        id_column (str): Name of the ID column
        record_id (int): ID of the record to update
        update_dict (dict): Dictionary of column names and new values
    """
    if not update_dict:
        return False

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()

            # Build SET clause dynamically from update_dict
            set_clause = ", ".join([f"{key} = %s" for key in update_dict.keys()])
            values = list(update_dict.values()) + [record_id]  # Add ID at the end for WHERE clause

            query = f"""
            UPDATE {table_name}
            SET {set_clause}
            WHERE {id_column} = %s
            """

            cursor.execute(query, values)
            conn.commit()
            return True
        except Error as e:
            st.error(f"Error updating record: {e}")
            return False
        finally:
            conn.close()
    return False

# Add this function to each page's tab section
def create_update_form(table_name, record_data, fields_info):
    """
    Creates a dynamic update form based on field information

    Args:
        table_name (str): Name of the table
        record_data (dict): Current record data
        fields_info (dict): Dictionary defining field types and options
    """
    update_data = {}

    for field, field_info in fields_info.items():
        field_type = field_info.get('type', 'text')
        current_value = record_data.get(field)

        if field_type == 'number':
            min_value = field_info.get('min_value', 0)
            new_value = st.number_input(
                field.replace('_', ' ').title(),
                min_value=min_value,
                value=current_value if current_value else min_value
            )
        elif field_type == 'date':
            new_value = st.date_input(
                field.replace('_', ' ').title(),
                value=current_value if current_value else None
            )
        elif field_type == 'select':
            options = field_info.get('options', [])
            new_value = st.selectbox(
                field.replace('_', ' ').title(),
                options=options,
                index=options.index(current_value) if current_value in options else 0
            )
        elif field_type == 'textarea':
            new_value = st.text_area(
                field.replace('_', ' ').title(),
                value=current_value if current_value else ''
            )
        else:  # Default to text input
            new_value = st.text_input(
                field.replace('_', ' ').title(),
                value=current_value if current_value else ''
            )

        if new_value != current_value and new_value != '':
            update_data[field] = new_value

    return update_data

def get_trial_information(trial_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc("GetTrialInformation", [trial_id])
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            return results
        except Error as e:
            st.error(f"Error fetching trial information: {e}")
            return None
        finally:
            conn.close()
    return None

def patient_page():
    st.title("Patient Management")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["View Patients", "Add Patient", "Update Patient", "Delete Patient", "Patient Visit Analysis"])

    with tab1:
        patients = fetch_all("Patient")
        if patients:
            df = pd.DataFrame(patients)
            st.dataframe(df)

    with tab2:
        with st.form("add_patient"):
            patient_id = st.number_input("Patient ID", min_value=1)
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            age = st.number_input("Age", min_value=18)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            dob = st.date_input("Date of Birth")
            contact = st.text_input("Contact Number")
            email = st.text_input("Email")
            address = st.text_area("Address")
            medical_history = st.text_area("Medical History")

            if st.form_submit_button("Add Patient"):
                conn = create_connection()
                if conn:
                    try:
                        cursor = conn.cursor()
                        query = """
                                INSERT INTO Patient (
                                    Patient_ID, First_Name, Last_Name, Age, Gender, Date_of_Birth, Contact_Number, Email, Address, Medical_History
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """
                        cursor.execute(query, (patient_id, first_name, last_name, age, gender,
                                            dob, contact, email, address, medical_history))
                        conn.commit()
                        st.success("Patient added successfully!")
                    except Error as e:
                        st.error(f"Error adding patient: {e}")
                    finally:
                        conn.close()

    with tab3:
        st.subheader("Update Patient")
        patients = fetch_all("Patient")
        if patients:
            selected_patient = st.selectbox(
                "Select Patient to Update",
                options=[(p['Patient_ID'], f"{p['Patient_ID']} - {p['First_Name']} {p['Last_Name']}") for p in patients],
                format_func=lambda x: x[1]
            )

            if selected_patient:
                current_patient = next(p for p in patients if p['Patient_ID'] == selected_patient[0])

                fields_info = {
                    'First_Name': {'type': 'text'},
                    'Last_Name': {'type': 'text'},
                    'Age': {'type': 'number', 'min_value': 18},
                    'Gender': {'type': 'select', 'options': ['Male', 'Female', 'Other']},
                    'Date_of_Birth': {'type': 'date'},
                    'Contact_Number': {'type': 'text'},
                    'Email': {'type': 'text'},
                    'Address': {'type': 'textarea'},
                    'Medical_History': {'type': 'textarea'}
                }

                with st.form("update_patient"):
                    update_data = create_update_form("Patient", current_patient, fields_info)

                    if st.form_submit_button("Update Patient"):
                        if update_data:
                            if update_record("Patient", "Patient_ID", selected_patient[0], update_data):
                                st.success("Patient updated successfully!")
                                st.rerun()
                        else:
                            st.warning("No changes made to update.")

    with tab4:
        patients = fetch_all("Patient")
        if patients:
            patient_to_delete = st.selectbox(
                "Select Patient to Delete",
                options=[(p['Patient_ID'], f"{p['Patient_ID']} - {p['First_Name']} {p['Last_Name']}") for p in patients],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Patient"):
                delete_record("Patient", "Patient_ID", patient_to_delete[0])

    with tab5:
        st.subheader("Patient Visit Analysis")
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                # Complex nested query for visit analysis
                query = """
                    SELECT
                        p.Patient_ID,
                        p.First_Name,
                        p.Last_Name,
                        (
                            SELECT COUNT(*)
                            FROM Visit v2
                            WHERE v2.Patient_ID = p.Patient_ID
                        ) as visit_count,
                        (
                            SELECT AVG(visit_count)
                            FROM (
                                SELECT COUNT(*) as visit_count
                                FROM Visit v3
                                GROUP BY v3.Patient_ID
                            ) as avg_visits
                        ) as avg_patient_visits,
                        (
                            SELECT COUNT(DISTINCT Doctor_ID)
                            FROM Visit v4
                            WHERE v4.Patient_ID = p.Patient_ID
                        ) as unique_doctors
                    FROM Patient p
                    WHERE EXISTS (
                        SELECT 1
                        FROM Visit v6
                        WHERE v6.Patient_ID = p.Patient_ID
                    )
                    ORDER BY visit_count DESC
                """
                cursor.execute(query)
                visit_analysis = cursor.fetchall()

                if visit_analysis:
                    for patient in visit_analysis:
                        with st.container():
                            st.subheader(f"{patient['First_Name']} {patient['Last_Name']}")
                            col1, col2, col3 = st.columns(3)

                            with col1:
                                visit_diff = patient['visit_count'] - patient['avg_patient_visits']
                                st.metric(
                                    "Total Visits",
                                    patient['visit_count'],
                                    f"{visit_diff:+.1f} vs avg",
                                    delta_color="off" if abs(visit_diff) < 2 else None
                                )

                            with col2:
                                st.metric("Average Visits", f"{patient['avg_patient_visits']:.1f}")

                            with col3:
                                st.metric("Unique Doctors", patient['unique_doctors'])

                            st.divider()
                else:
                    st.info("No visit data available for analysis.")
            except Error as e:
                st.error(f"Error analyzing visits: {e}")
            finally:
                conn.close()

def doctor_page():
    st.title("Doctor Management")

    tab1, tab2, tab3, tab4 = st.tabs(["View Doctors", "Add Doctor", "Update Doctor", "Delete Doctor"])

    with tab1:
        doctors = fetch_all("Doctor")
        if doctors:
            df = pd.DataFrame(doctors)
            st.dataframe(df)

    with tab2:
        with st.form("add_doctor"):
            doctor_id = st.number_input("Doctor ID", min_value=1)
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            specialization = st.text_input("Specialization")
            contact = st.text_input("Contact Number")
            email = st.text_input("Email")
            lab_id = st.number_input("Lab ID", min_value=1)

            if st.form_submit_button("Add Doctor"):
                conn = create_connection()
                if conn:
                    try:
                        cursor = conn.cursor()
                        query = """
                                INSERT INTO Doctor (
                                    Doctor_ID, First_Name, Last_Name, Specialization, Contact_Number, Email, Lab_ID
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """
                        cursor.execute(query, (doctor_id, first_name, last_name,
                                            specialization, contact, email, lab_id))
                        conn.commit()
                        st.success("Doctor added successfully!")
                    except Error as e:
                        st.error(f"Error adding doctor: {e}")
                    finally:
                        conn.close()

    with tab3:
        st.subheader("Update Doctor")
        doctors = fetch_all("Doctor")
        if doctors:
            selected_doctor = st.selectbox(
                "Select Doctor to Update",
                options=[(d['Doctor_ID'], f"{d['Doctor_ID']} - {d['First_Name']} {d['Last_Name']}") for d in doctors],
                format_func=lambda x: x[1]
            )

            if selected_doctor:
                current_doctor = next(d for d in doctors if d['Doctor_ID'] == selected_doctor[0])

                fields_info = {
                    'First_Name': {'type': 'text'},
                    'Last_Name': {'type': 'text'},
                    'Specialization': {'type': 'text'},
                    'Contact_Number': {'type': 'text'},
                    'Email': {'type': 'text'},
                    'Lab_ID': {'type': 'number', 'min_value': 1}
                }

                with st.form("update_doctor"):
                    update_data = create_update_form("Doctor", current_doctor, fields_info)

                    if st.form_submit_button("Update Doctor"):
                        if update_data:
                            if update_record("Doctor", "Doctor_ID", selected_doctor[0], update_data):
                                st.success("Doctor updated successfully!")
                                st.rerun()
                        else:
                            st.warning("No changes made to update.")

    with tab4:
        doctors = fetch_all("Doctor")
        if doctors:
            doctor_to_delete = st.selectbox(
                "Select Doctor to Delete",
                options=[(d['Doctor_ID'], f"{d['Doctor_ID']} - {d['First_Name']} {d['Last_Name']}") for d in doctors],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Doctor"):
                delete_record("Doctor", "Doctor_ID", doctor_to_delete[0])

def visit_page():
    st.title("Visit Management")

    # Fetch patients and doctors for dropdowns
    patients = fetch_all("Patient")
    doctors = fetch_all("Doctor")

    # Create patient and doctor mapping for easy lookup
    # patient_map = {p['Patient_ID']: f"{p['First_Name']} {p['Last_Name']}" for p in patients}
    # doctor_map = {d['Doctor_ID']: f"Dr. {d['First_Name']} {d['Last_Name']}" for d in doctors}

    tab1, tab2, tab3, tab4 = st.tabs(["View Visits", "Add Visit", "Update Visit", "Delete Visit"])

    with tab1:
        # Fetch visits with joined patient and doctor information
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT v.*,
                           CONCAT(p.First_Name, ' ', p.Last_Name) as Patient_Name,
                           CONCAT('Dr. ', d.First_Name, ' ', d.Last_Name) as Doctor_Name
                    FROM Visit v
                    JOIN Patient p ON v.Patient_ID = p.Patient_ID
                    JOIN Doctor d ON v.Doctor_ID = d.Doctor_ID
                """
                cursor.execute(query)
                visits = cursor.fetchall()
                if visits:
                    df = pd.DataFrame(visits)
                    st.dataframe(df)
            finally:
                conn.close()

    with tab2:
        with st.form("add_visit"):
            visit_id = st.number_input("Visit ID", min_value=1)

            # Patient dropdown with names
            selected_patient = st.selectbox(
                "Select Patient",
                options=[(p['Patient_ID'], f"{p['Patient_ID']} - {p['First_Name']} {p['Last_Name']}") for p in patients],
                format_func=lambda x: x[1]
            )
            patient_id = selected_patient[0] if selected_patient else None

            # Doctor dropdown with names
            selected_doctor = st.selectbox(
                "Select Doctor",
                options=[(d['Doctor_ID'], f"{d['Doctor_ID']} - Dr. {d['First_Name']} {d['Last_Name']}") for d in doctors],
                format_func=lambda x: x[1]
            )
            doctor_id = selected_doctor[0] if selected_doctor else None

            visit_date = st.date_input("Visit Date")
            visit_details = st.text_area("Visit Details")

            if st.form_submit_button("Add Visit"):
                conn = create_connection()
                if conn and patient_id and doctor_id:
                    try:
                        cursor = conn.cursor()
                        query = """
                                INSERT INTO Visit (
                                    Visit_ID, Patient_ID, Doctor_ID, Visit_Date, Visit_Details
                                ) VALUES (%s, %s, %s, %s, %s)
                                """
                        cursor.execute(query, (visit_id, patient_id, doctor_id,
                                            visit_date, visit_details))
                        conn.commit()
                        st.success("Visit added successfully!")
                    except Error as e:
                        st.error(f"Error adding visit: {e}")
                    finally:
                        conn.close()

    with tab3:
        st.subheader("Update Visit")
        # Fetch visits with joined information
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT v.*,
                           CONCAT(p.First_Name, ' ', p.Last_Name) as Patient_Name,
                           CONCAT('Dr. ', d.First_Name, ' ', d.Last_Name) as Doctor_Name
                    FROM Visit v
                    JOIN Patient p ON v.Patient_ID = p.Patient_ID
                    JOIN Doctor d ON v.Doctor_ID = d.Doctor_ID
                """
                cursor.execute(query)
                visits = cursor.fetchall()

                if visits:
                    selected_visit = st.selectbox(
                        "Select Visit to Update",
                        options=[(v['Visit_ID'], f"Visit {v['Visit_ID']} - {v['Patient_Name']} with {v['Doctor_Name']}") for v in visits],
                        format_func=lambda x: x[1]
                    )

                    if selected_visit:
                        current_visit = next(v for v in visits if v['Visit_ID'] == selected_visit[0])

                        with st.form("update_visit"):
                            # Patient dropdown with current selection
                            updated_patient = st.selectbox(
                                "Patient",
                                options=[(p['Patient_ID'], f"{p['Patient_ID']} - {p['First_Name']} {p['Last_Name']}") for p in patients],
                                format_func=lambda x: x[1],
                                index=[i for i, p in enumerate(patients) if p['Patient_ID'] == current_visit['Patient_ID']][0]
                            )

                            # Doctor dropdown with current selection
                            updated_doctor = st.selectbox(
                                "Doctor",
                                options=[(d['Doctor_ID'], f"{d['Doctor_ID']} - Dr. {d['First_Name']} {d['Last_Name']}") for d in doctors],
                                format_func=lambda x: x[1],
                                index=[i for i, d in enumerate(doctors) if d['Doctor_ID'] == current_visit['Doctor_ID']][0]
                            )

                            updated_date = st.date_input("Visit Date", value=current_visit['Visit_Date'])
                            updated_details = st.text_area("Visit Details", value=current_visit['Visit_Details'])

                            if st.form_submit_button("Update Visit"):
                                update_data = {
                                    'Patient_ID': updated_patient[0],
                                    'Doctor_ID': updated_doctor[0],
                                    'Visit_Date': updated_date,
                                    'Visit_Details': updated_details
                                }

                                if update_record("Visit", "Visit_ID", selected_visit[0], update_data):
                                    st.success("Visit updated successfully!")
                                    st.rerun()
            finally:
                conn.close()

    with tab4:
        # Fetch visits with joined information for delete
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT v.*,
                           CONCAT(p.First_Name, ' ', p.Last_Name) as Patient_Name,
                           CONCAT('Dr. ', d.First_Name, ' ', d.Last_Name) as Doctor_Name
                    FROM Visit v
                    JOIN Patient p ON v.Patient_ID = p.Patient_ID
                    JOIN Doctor d ON v.Doctor_ID = d.Doctor_ID
                """
                cursor.execute(query)
                visits = cursor.fetchall()

                if visits:
                    visit_to_delete = st.selectbox(
                        "Select Visit to Delete",
                        options=[(v['Visit_ID'], f"Visit {v['Visit_ID']} - {v['Patient_Name']} with {v['Doctor_Name']}") for v in visits],
                        format_func=lambda x: x[1]
                    )
                    if st.button("Delete Visit"):
                        delete_record("Visit", "Visit_ID", visit_to_delete[0])
            finally:
                conn.close()

def laboratory_page():
    st.title("Laboratory Management")

    tab1, tab2, tab3, tab4 = st.tabs(["View Laboratories", "Add Laboratory", "Update Laboratory", "Delete Laboratory"])

    with tab1:
        labs = fetch_all("Laboratory")
        if labs:
            df = pd.DataFrame(labs)
            st.dataframe(df)

    with tab2:
        with st.form("add_laboratory"):
            lab_id = st.number_input("Lab ID", min_value=1)
            name = st.text_input("Laboratory Name")
            location = st.text_input("Location")
            contact = st.text_input("Contact Number")
            email = st.text_input("Email")

            if st.form_submit_button("Add Laboratory"):
                conn = create_connection()
                if conn:
                    try:
                        cursor = conn.cursor()
                        query = """
                        INSERT INTO Laboratory (
                          Lab_ID, Name, Location, Contact_Number, Email
                        ) VALUES (%s, %s, %s, %s, %s)
                        """
                        cursor.execute(query, (lab_id, name, location, contact, email))
                        conn.commit()
                        st.success("Laboratory added successfully!")
                    except Error as e:
                        st.error(f"Error adding laboratory: {e}")
                    finally:
                        conn.close()

    with tab3:
        st.subheader("Update Laboratory")
        labs = fetch_all("Laboratory")
        if labs:
            selected_lab = st.selectbox(
                "Select Laboratory to Update",
                options=[(l['Lab_ID'], f"{l['Lab_ID']} - {l['Name']}") for l in labs],
                format_func=lambda x: x[1]
            )

            if selected_lab:
                current_lab = next(l for l in labs if l['Lab_ID'] == selected_lab[0])

                fields_info = {
                    'Name': {'type': 'text'},
                    'Location': {'type': 'text'},
                    'Contact_Number': {'type': 'text'},
                    'Email': {'type': 'text'}
                }

                with st.form("update_laboratory"):
                    update_data = create_update_form("Laboratory", current_lab, fields_info)

                    if st.form_submit_button("Update Laboratory"):
                        if update_data:
                            if update_record("Laboratory", "Lab_ID", selected_lab[0], update_data):
                                st.success("Laboratory updated successfully!")
                                st.rerun()
                        else:
                            st.warning("No changes made to update.")

    with tab4:
        labs = fetch_all("Laboratory")
        if labs:
            lab_to_delete = st.selectbox(
                "Select Laboratory to Delete",
                options=[(l['Lab_ID'], f"{l['Lab_ID']} - {l['Name']}") for l in labs],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Laboratory"):
                delete_record("Laboratory", "Lab_ID", lab_to_delete[0])

def manufacturer_page():
    st.title("Manufacturer Management")

    tab1, tab2, tab3, tab4 = st.tabs(["View Manufacturers", "Add Manufacturer", "Update Manufacturer", "Delete Manufacturer"])

    with tab1:
        manufacturers = fetch_all("Manufacturer")
        if manufacturers:
            df = pd.DataFrame(manufacturers)
            st.dataframe(df)

    with tab2:
        with st.form("add_manufacturer"):
            manufacturer_id = st.number_input("Manufacturer ID", min_value=1)
            name = st.text_input("Manufacturer Name")
            email = st.text_input("Email")
            contact = st.text_input("Contact Number")
            address = st.text_area("Address")

            if st.form_submit_button("Add Manufacturer"):
                conn = create_connection()
                if conn:
                    try:
                        cursor = conn.cursor()
                        query = """
                        INSERT INTO Manufacturer (
                            Manufacturer_ID, Name, Email, Contact_Number, Address
                        ) VALUES (%s, %s, %s, %s, %s)
                        """
                        cursor.execute(query, (manufacturer_id, name, email, contact, address))
                        conn.commit()
                        st.success("Manufacturer added successfully!")
                    except Error as e:
                        st.error(f"Error adding manufacturer: {e}")
                    finally:
                        conn.close()

    with tab3:
        st.subheader("Update Manufacturer")
        manufacturers = fetch_all("Manufacturer")
        if manufacturers:
            selected_manufacturer = st.selectbox(
                "Select Manufacturer to Update",
                options=[(m['Manufacturer_ID'], f"{m['Manufacturer_ID']} - {m['Name']}") for m in manufacturers],
                format_func=lambda x: x[1]
            )

            if selected_manufacturer:
                current_manufacturer = next(m for m in manufacturers if m['Manufacturer_ID'] == selected_manufacturer[0])

                fields_info = {
                    'Name': {'type': 'text'},
                    'Email': {'type': 'text'},
                    'Contact_Number': {'type': 'text'},
                    'Address': {'type': 'textarea'}
                }

                with st.form("update_manufacturer"):
                    update_data = create_update_form("Manufacturer", current_manufacturer, fields_info)

                    if st.form_submit_button("Update Manufacturer"):
                        if update_data:
                            if update_record("Manufacturer", "Manufacturer_ID", selected_manufacturer[0], update_data):
                                st.success("Manufacturer updated successfully!")
                                st.rerun()
                        else:
                            st.warning("No changes made to update.")

    with tab4:
        manufacturers = fetch_all("Manufacturer")
        if manufacturers:
            manufacturer_to_delete = st.selectbox(
                "Select Manufacturer to Delete",
                options=[(m['Manufacturer_ID'], f"{m['Manufacturer_ID']} - {m['Name']}") for m in manufacturers],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Manufacturer"):
                delete_record("Manufacturer", "Manufacturer_ID", manufacturer_to_delete[0])

def medication_page():
    st.title("Medication Management")

    tab1, tab2, tab3, tab4 = st.tabs(["View Medications", "Add Medication", "Update Medication", "Delete Medication"])

    with tab1:
        medications = fetch_all("Medication")
        if medications:
            df = pd.DataFrame(medications)
            st.dataframe(df)

    with tab2:
        with st.form("add_medication"):
            medication_id = st.number_input("Medication ID", min_value=1)
            name = st.text_input("Medication Name")
            manufacturer_id = st.number_input("Manufacturer ID", min_value=1)
            dosage = st.text_input("Dosage")
            side_effects = st.text_area("Side Effects")
            frequency = st.text_input("Frequency")
            admin_method = st.text_input("Administration Method")

            if st.form_submit_button("Add Medication"):
                conn = create_connection()
                if conn:
                    try:
                        cursor = conn.cursor()
                        query = """
                        INSERT INTO Medication (
                            Medication_ID, Name, Manufacturer_ID, Dosage, Side_Effects, Frequency, Administration_Method
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(query, (medication_id, name, manufacturer_id,
                                            dosage, side_effects, frequency, admin_method))
                        conn.commit()
                        st.success("Medication added successfully!")
                    except Error as e:
                        st.error(f"Error adding medication: {e}")
                    finally:
                        conn.close()

    with tab3:
        st.subheader("Update Medication")
        medications = fetch_all("Medication")
        if medications:
            selected_medication = st.selectbox(
                "Select Medication to Update",
                options=[(m['Medication_ID'], f"{m['Medication_ID']} - {m['Name']}") for m in medications],
                format_func=lambda x: x[1]
            )

            if selected_medication:
                current_medication = next(m for m in medications if m['Medication_ID'] == selected_medication[0])

                fields_info = {
                    'Name': {'type': 'text'},
                    'Manufacturer_ID': {'type': 'number', 'min_value': 1},
                    'Dosage': {'type': 'text'},
                    'Side_Effects': {'type': 'textarea'},
                    'Frequency': {'type': 'text'},
                    'Administration_Method': {'type': 'text'}
                }

                with st.form("update_medication"):
                    update_data = create_update_form("Medication", current_medication, fields_info)

                    if st.form_submit_button("Update Medication"):
                        if update_data:
                            if update_record("Medication", "Medication_ID", selected_medication[0], update_data):
                                st.success("Medication updated successfully!")
                                st.rerun()
                        else:
                            st.warning("No changes made to update.")

    with tab4:
        medications = fetch_all("Medication")
        if medications:
            medication_to_delete = st.selectbox(
                "Select Medication to Delete",
                options=[(m['Medication_ID'], f"{m['Medication_ID']} - {m['Name']}") for m in medications],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Medication"):
                delete_record("Medication", "Medication_ID", medication_to_delete[0])

def clinical_trial_page():
    st.title("Clinical Trial Management")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["View Clinical Trials", "Trial Details", "Add Clinical Trial", "Update Clinical Trial", "Delete Clinical Trial"]) # noqa

    with tab1:
        trials = fetch_all("Clinical_Trial")
        if trials:
            df = pd.DataFrame(trials)
            st.dataframe(df)

    with tab2:
        st.subheader("Trial Information")
        trials = fetch_all("Clinical_Trial")

        if trials:
            selected_trial = st.selectbox(
                "Select Trial to View Details",
                options=[(t["Trial_ID"], f"{t['Trial_ID']} - {t['Trial_Name']}") for t in trials],
                format_func=lambda x: f"{x[0]} - {x[1]}"
            )

            if selected_trial:
                trial_data = get_trial_information(selected_trial[0])

                if trial_data and len(trial_data) > 0:
                    trial_info = trial_data[0]

                    col1, col2 = st.columns(2)

                    with col1:
                        with st.expander("Trial Information", expanded=True):
                            st.write("**Trial ID:**", trial_info['Trial_ID'])
                            st.write("**Trial Name:**", trial_info['Trial_Name'])
                            st.write("**Description:**", trial_info['Description'])
                            st.write("**Start Date:**", trial_info['Trial_Start_Date'])
                            st.write("**End Date:**", trial_info['Trial_End_Date'])

                        with st.expander("Patient Information", expanded=True):
                            st.write("**Patient ID:**", trial_info['Patient_ID'])
                            st.write("**Patient Name:**",
                                   f"{trial_info['Patient_First_Name']} {trial_info['Patient_Last_Name']}")

                    with col2:
                        with st.expander("Doctor Information", expanded=True):
                            st.write("**Doctor ID:**", trial_info['Doctor_ID'])
                            st.write("**Doctor Name:**",
                                   f"{trial_info['Doctor_First_Name']} {trial_info['Doctor_Last_Name']}")
                            st.write("**Specialization:**", trial_info['Specialization'])

                        with st.expander("Medication Information", expanded=True):
                            st.write("**Medication ID:**", trial_info['Medication_ID'])
                            st.write("**Medication Name:**", trial_info['Medication_Name'])
                            st.write("**Dosage:**", trial_info['Dosage'])
                            st.write("**Administration Method:**", trial_info['Administration_Method'])
                            st.write("**Side Effects:**", trial_info['Side_Effects'])

                    with st.expander("Results Information", expanded=True):
                        if trial_info['Result_ID']:
                            st.write("**Result ID:**", trial_info['Result_ID'])
                            st.write("**Result Date:**", trial_info['Result_Date'])
                            st.write("**Result Details:**", trial_info['Result_Details'])
                            st.write("**Laboratory ID:**", trial_info['Lab_ID'])
                            st.write("**Laboratory Name:**", trial_info['Lab_Name'])
                        else:
                            st.info("No results recorded for this trial yet.")
                else:
                    st.warning("No detailed information found for this trial.")
        else:
            st.info("No trials available to view.")

    with tab3:
        with st.form("add_clinical_trial"):
            trial_id = st.number_input("Trial ID", min_value=1)
            trial_name = st.text_input("Trial Name")
            description = st.text_area("Description")
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            patient_id = st.number_input("Patient ID", min_value=1)
            medication_id = st.number_input("Medication ID", min_value=1)
            doctor_id = st.number_input("Doctor ID", min_value=1)

            if st.form_submit_button("Add Clinical Trial"):
                conn = create_connection()
                if conn:
                    try:
                        cursor = conn.cursor()
                        query = """
                        INSERT INTO Clinical_Trial (
                            Trial_ID, Trial_Name, Description, Trial_Start_Date, Trial_End_Date, Patient_ID, Medication_ID, Doctor_ID
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(query, (trial_id, trial_name, description,
                                            start_date, end_date, patient_id,
                                            medication_id, doctor_id))
                        conn.commit()
                        st.success("Clinical Trial added successfully!")
                    except Error as e:
                        st.error(f"Error adding clinical trial: {e}")
                    finally:
                        conn.close()

    with tab4:
        st.subheader("Update Clinical Trial")
        trials = fetch_all("Clinical_Trial")
        if trials:
            selected_trial = st.selectbox(
                "Select Clinical Trial to Update",
                options=[(t['Trial_ID'], f"{t['Trial_ID']} - {t['Trial_Name']}") for t in trials],
                format_func=lambda x: x[1]
            )

            if selected_trial:
                current_trial = next(t for t in trials if t['Trial_ID'] == selected_trial[0])

                fields_info = {
                    'Trial_Name': {'type': 'text'},
                    'Description': {'type': 'textarea'},
                    'Trial_Start_Date': {'type': 'date'},
                    'Trial_End_Date': {'type': 'date'},
                    'Patient_ID': {'type': 'number', 'min_value': 1},
                    'Medication_ID': {'type': 'number', 'min_value': 1},
                    'Doctor_ID': {'type': 'number', 'min_value': 1}
                }

                with st.form("update_trial"):
                    update_data = create_update_form("Clinical_Trial", current_trial, fields_info)

                    if st.form_submit_button("Update Clinical Trial"):
                        if update_data:
                            if update_record("Clinical_Trial", "Trial_ID", selected_trial[0], update_data):
                                st.success("Clinical Trial updated successfully!")
                                st.rerun()
                        else:
                            st.warning("No changes made to update.")

    with tab5:
        trials = fetch_all("Clinical_Trial")
        if trials:
            trial_to_delete = st.selectbox(
                "Select Clinical Trial to Delete",
                options=[(t['Trial_ID'], f"{t['Trial_ID']} - {t['Trial_Name']}") for t in trials],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Clinical Trial"):
                delete_record("Clinical_Trial", "Trial_ID", trial_to_delete[0])

def results_page():
    st.title("Results Management")

    tab1, tab2, tab3, tab4 = st.tabs(["View Results", "Add Result", "Update Result", "Delete Result"])

    with tab1:
        results = fetch_all("Results")
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)

    with tab2:
        with st.form("add_result"):
            result_id = st.number_input("Result ID", min_value=1)
            trial_id = st.number_input("Trial ID", min_value=1)
            lab_id = st.number_input("Lab ID", min_value=1)
            patient_id = st.number_input("Patient ID", min_value=1)
            result_date = st.date_input("Result Date")
            result_details = st.text_area("Result Details")

            if st.form_submit_button("Add Result"):
                conn = create_connection()
                if conn:
                    try:
                        cursor = conn.cursor()
                        query = """
                        INSERT INTO Results (
                            Result_ID, Trial_ID, Lab_ID, Patient_ID, Result_Date, Result_Details
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(query, (result_id, trial_id, lab_id,
                                            patient_id, result_date, result_details))
                        conn.commit()
                        st.success("Result added successfully!")
                    except Error as e:
                        st.error(f"Error adding result: {e}")
                    finally:
                        conn.close()

    with tab3:
        st.subheader("Update Result")
        results = fetch_all("Results")
        if results:
            selected_result = st.selectbox(
                "Select Result to Update",
                options=[(r['Result_ID'], f"Result {r['Result_ID']} - Trial {r['Trial_ID']}") for r in results],
                format_func=lambda x: x[1]
            )

            if selected_result:
                current_result = next(r for r in results if r['Result_ID'] == selected_result[0])

                fields_info = {
                    'Trial_ID': {'type': 'number', 'min_value': 1},
                    'Lab_ID': {'type': 'number', 'min_value': 1},
                    'Patient_ID': {'type': 'number', 'min_value': 1},
                    'Result_Date': {'type': 'date'},
                    'Result_Details': {'type': 'textarea'}
                }

                with st.form("update_result"):
                    update_data = create_update_form("Results", current_result, fields_info)

                    if st.form_submit_button("Update Result"):
                        if update_data:
                            if update_record("Results", "Result_ID", selected_result[0], update_data):
                                st.success("Result updated successfully!")
                                st.rerun()
                        else:
                            st.warning("No changes made to update.")

    with tab4:
        results = fetch_all("Results")
        if results:
            result_to_delete = st.selectbox(
                "Select Result to Delete",
                options=[(r['Result_ID'], f"Result {r['Result_ID']} - Trial {r['Trial_ID']}") for r in results],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Result"):
                delete_record("Results", "Result_ID", result_to_delete[0])

def reactions_page():
    st.title("Reactions Management")

    tab1, tab2, tab3, tab4 = st.tabs(["View Reactions", "Add Reaction", "Update Reaction", "Delete Reaction"])

    with tab1:
        reactions = fetch_all("Reactions")
        if reactions:
            df = pd.DataFrame(reactions)
            st.dataframe(df)

    with tab2:
        with st.form("add_reaction"):
            reaction_id = st.number_input("Reaction ID", min_value=1)
            patient_id = st.number_input("Patient ID", min_value=1)
            medication_id = st.number_input("Medication ID", min_value=1)
            reaction_details = st.text_area("Reaction Details")
            reaction_date = st.date_input("Date of Reaction")

            if st.form_submit_button("Add Reaction"):
                conn = create_connection()
                if conn:
                    try:
                        cursor = conn.cursor()
                        query = """
                        INSERT INTO Reactions (
                            Reaction_ID, Patient_ID, Medication_ID, Reaction_Details, Date_of_Reaction
                        ) VALUES (%s, %s, %s, %s, %s)
                        """
                        cursor.execute(query, (reaction_id, patient_id, medication_id,
                                            reaction_details, reaction_date))
                        conn.commit()
                        st.success("Reaction added successfully!")
                    except Error as e:
                        st.error(f"Error adding reaction: {e}")
                    finally:
                        conn.close()

    with tab3:
        st.subheader("Update Reaction")
        reactions = fetch_all("Reactions")
        if reactions:
            selected_reaction = st.selectbox(
                "Select Reaction to Update",
                options=[(r['Reaction_ID'], f"Reaction {r['Reaction_ID']} - Patient {r['Patient_ID']}") for r in reactions],
                format_func=lambda x: x[1]
            )

            if selected_reaction:
                current_reaction = next(r for r in reactions if r['Reaction_ID'] == selected_reaction[0])

                fields_info = {
                    'Patient_ID': {'type': 'number', 'min_value': 1},
                    'Medication_ID': {'type': 'number', 'min_value': 1},
                    'Reaction_Details': {'type': 'textarea'},
                    'Date_of_Reaction': {'type': 'date'}
                }

                with st.form("update_reaction"):
                    update_data = create_update_form("Reactions", current_reaction, fields_info)

                    if st.form_submit_button("Update Reaction"):
                        if update_data:
                            if update_record("Reactions", "Reaction_ID", selected_reaction[0], update_data):
                                st.success("Reaction updated successfully!")
                                st.rerun()
                        else:
                            st.warning("No changes made to update.")

    with tab4:
        reactions = fetch_all("Reactions")
        if reactions:
            reaction_to_delete = st.selectbox(
                "Select Reaction to Delete",
                options=[(r['Reaction_ID'], f"Reaction {r['Reaction_ID']} - Patient {r['Patient_ID']}") for r in reactions],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Reaction"):
                delete_record("Reactions", "Reaction_ID", reaction_to_delete[0])

def main():
    st.set_page_config(page_title="Medical Database Management", layout="wide")

    sidebar_nav()

    if st.session_state.current_page == 'Home':
        st.title("Medical Database Management System")
        st.write("""
        Welcome to the Medical Database Management System.
        Use the sidebar to navigate through different sections.
        """)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            patients = fetch_all("Patient")
            st.metric("Total Patients", len(patients))

        with col2:
            doctors = fetch_all("Doctor")
            st.metric("Total Doctors", len(doctors))

        with col3:
            medications = fetch_all("Medication")
            st.metric("Total Medications", len(medications))

        with col4:
            trials = fetch_all("Clinical_Trial")
            st.metric("Active Trials", len(trials))

    elif st.session_state.current_page == 'Patients':
        patient_page()
    elif st.session_state.current_page == 'Doctors':
        doctor_page()
    elif st.session_state.current_page == 'Laboratories':
        laboratory_page()
    elif st.session_state.current_page == 'Visits':
        visit_page()
    elif st.session_state.current_page == 'Medications':
        medication_page()
    elif st.session_state.current_page == 'Manufacturers':
        manufacturer_page()
    elif st.session_state.current_page == 'Clinical Trials':
        clinical_trial_page()
    elif st.session_state.current_page == 'Results':
        results_page()
    elif st.session_state.current_page == 'Reactions':
        reactions_page()

if __name__ == "__main__":
    main()
