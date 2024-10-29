import streamlit as st
import mysql.connector
import requests
from mysql.connector import Error
import pandas as pd

# Database connection
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

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

# Sidebar navigation
def sidebar_nav():
    st.sidebar.title("Navigation")
    pages = ['Home', 'Patients', 'Doctors', 'Laboratories', 'Visits',
             'Medications', 'Manufacturers', 'Clinical Trials', 'Results', 'Reactions']
    st.session_state.current_page = st.sidebar.radio("Go to", pages)

# Generic functions for database operations
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

# Patient Management
def patient_page():
    st.title("Patient Management")

    tab1, tab2, tab3 = st.tabs(["View Patients", "Add Patient", "Delete Patient"])

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
        patients = fetch_all("Patient")
        if patients:
            patient_to_delete = st.selectbox(
                "Select Patient to Delete",
                options=[(p['Patient_ID'], f"{p['First_Name']} {p['Last_Name']}") for p in patients],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Patient"):
                delete_record("Patient", "Patient_ID", patient_to_delete[0])

# Doctor Management
def doctor_page():
    st.title("Doctor Management")

    tab1, tab2, tab3 = st.tabs(["View Doctors", "Add Doctor", "Delete Doctor"])

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
        doctors = fetch_all("Doctor")
        if doctors:
            doctor_to_delete = st.selectbox(
                "Select Doctor to Delete",
                options=[(d['Doctor_ID'], f"{d['First_Name']} {d['Last_Name']}") for d in doctors],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Doctor"):
                delete_record("Doctor", "Doctor_ID", doctor_to_delete[0])

# Visit Management
def visit_page():
    st.title("Visit Management")

    tab1, tab2, tab3 = st.tabs(["View Visits", "Add Visit", "Delete Visit"])

    with tab1:
        visits = fetch_all("Visit")
        if visits:
            df = pd.DataFrame(visits)
            st.dataframe(df)

    with tab2:
        with st.form("add_visit"):
            visit_id = st.number_input("Visit ID", min_value=1)
            patient_id = st.number_input("Patient ID", min_value=1)
            doctor_id = st.number_input("Doctor ID", min_value=1)
            visit_date = st.date_input("Visit Date")
            visit_details = st.text_area("Visit Details")

            if st.form_submit_button("Add Visit"):
                conn = create_connection()
                if conn:
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
        visits = fetch_all("Visit")
        if visits:
            visit_to_delete = st.selectbox(
                "Select Visit to Delete",
                options=[(v['Visit_ID'], f"Visit {v['Visit_ID']} - Patient {v['Patient_ID']}") for v in visits],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Visit"):
                delete_record("Visit", "Visit_ID", visit_to_delete[0])

# Laboratory Management
def laboratory_page():
    st.title("Laboratory Management")

    tab1, tab2, tab3 = st.tabs(["View Laboratories", "Add Laboratory", "Delete Laboratory"])

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
        labs = fetch_all("Laboratory")
        if labs:
            lab_to_delete = st.selectbox(
                "Select Laboratory to Delete",
                options=[(l['Lab_ID'], l['Name']) for l in labs],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Laboratory"):
                delete_record("Laboratory", "Lab_ID", lab_to_delete[0])

# Manufacturer Management
def manufacturer_page():
    st.title("Manufacturer Management")

    tab1, tab2, tab3 = st.tabs(["View Manufacturers", "Add Manufacturer", "Delete Manufacturer"])

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
        manufacturers = fetch_all("Manufacturer")
        if manufacturers:
            manufacturer_to_delete = st.selectbox(
                "Select Manufacturer to Delete",
                options=[(m['Manufacturer_ID'], m['Name']) for m in manufacturers],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Manufacturer"):
                delete_record("Manufacturer", "Manufacturer_ID", manufacturer_to_delete[0])

# Medication Management
def medication_page():
    st.title("Medication Management")

    tab1, tab2, tab3 = st.tabs(["View Medications", "Add Medication", "Delete Medication"])

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
        medications = fetch_all("Medication")
        if medications:
            medication_to_delete = st.selectbox(
                "Select Medication to Delete",
                options=[(m['Medication_ID'], m['Name']) for m in medications],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Medication"):
                delete_record("Medication", "Medication_ID", medication_to_delete[0])

# # Clinical Trial Management
# def clinical_trial_page():
#     st.title("Clinical Trial Management")
#
#     tab1, tab2, tab3 = st.tabs(["View Clinical Trials", "Add Clinical Trial", "Delete Clinical Trial"])
#
#     with tab1:
#         trials = fetch_all("Clinical_Trial")
#         if trials:
#             df = pd.DataFrame(trials)
#             st.dataframe(df)
#
#     with tab2:
#         with st.form("add_clinical_trial"):
#             trial_id = st.number_input("Trial ID", min_value=1)
#             trial_name = st.text_input("Trial Name")
#             description = st.text_area("Description")
#             start_date = st.date_input("Start Date")
#             end_date = st.date_input("End Date")
#             patient_id = st.number_input("Patient ID", min_value=1)
#             medication_id = st.number_input("Medication ID", min_value=1)
#             doctor_id = st.number_input("Doctor ID", min_value=1)
#
#             if st.form_submit_button("Add Clinical Trial"):
#                 conn = create_connection()
#                 if conn:
#                     try:
#                         cursor = conn.cursor()
#                         query = """
#                         INSERT INTO Clinical_Trial (
#                             Trial_ID, Trial_Name, Description, Trial_Start_Date, Trial_End_Date, Patient_ID, Medication_ID, Doctor_ID
#                         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#                         """
#                         cursor.execute(query, (trial_id, trial_name, description,
#                                             start_date, end_date, patient_id,
#                                             medication_id, doctor_id))
#                         conn.commit()
#                         st.success("Clinical Trial added successfully!")
#                     except Error as e:
#                         st.error(f"Error adding clinical trial: {e}")
#                     finally:
#                         conn.close()
#
#     with tab3:
#         trials = fetch_all("Clinical_Trial")
#         if trials:
#             trial_to_delete = st.selectbox(
#                 "Select Clinical Trial to Delete",
#                 options=[(t['Trial_ID'], t['Trial_Name']) for t in trials],
#                 format_func=lambda x: x[1]
#             )
#             if st.button("Delete Clinical Trial"):
#                 delete_record("Clinical_Trial", "Trial_ID", trial_to_delete[0])

def clinical_trial_page():
    st.title("Clinical Trial Management")

    tab1, tab2, tab3, tab4 = st.tabs(["View Clinical Trials", "Trial Details", "Add Clinical Trial", "Delete Clinical Trial"])

    with tab1:
        trials = fetch_all("Clinical_Trial")
        if trials:
            df = pd.DataFrame(trials)
            st.dataframe(df)

    with tab2:
        st.subheader("Trial Information")
        # Get list of trials for selection
        trials = fetch_all("Clinical_Trial")
        if trials:
            selected_trial = st.selectbox(
                "Select Trial to View Details",
                options=[(t['Trial_ID'], t['Trial_Name']) for t in trials],
                format_func=lambda x: f"{x[0]} - {x[1]}"
            )
            
            if selected_trial:
                # Fetch detailed trial information
                try:
                    response = requests.get(f"http://localhost:5000/api/trial_information/{selected_trial[0]}")
                    if response.status_code == 200:
                        trial_data = response.json()['data']
                        if trial_data:
                            trial_info = trial_data[0]  # Get the first (and should be only) result
                            
                            # Display information in organized sections using columns and expanders
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
                            
                            # Results and Laboratory information in full width
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
                        st.error("Failed to fetch trial information.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the backend: {str(e)}")
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
        trials = fetch_all("Clinical_Trial")
        if trials:
            trial_to_delete = st.selectbox(
                "Select Clinical Trial to Delete",
                options=[(t['Trial_ID'], t['Trial_Name']) for t in trials],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Clinical Trial"):
                delete_record("Clinical_Trial", "Trial_ID", trial_to_delete[0])

# Results Management
def results_page():
    st.title("Results Management")

    tab1, tab2, tab3 = st.tabs(["View Results", "Add Result", "Delete Result"])

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
        results = fetch_all("Results")
        if results:
            result_to_delete = st.selectbox(
                "Select Result to Delete",
                options=[(r['Result_ID'], f"Result {r['Result_ID']} - Trial {r['Trial_ID']}") for r in results],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Result"):
                delete_record("Results", "Result_ID", result_to_delete[0])

# Reactions Management
def reactions_page():
    st.title("Reactions Management")

    tab1, tab2, tab3 = st.tabs(["View Reactions", "Add Reaction", "Delete Reaction"])

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
        reactions = fetch_all("Reactions")
        if reactions:
            reaction_to_delete = st.selectbox(
                "Select Reaction to Delete",
                options=[(r['Reaction_ID'], f"Reaction {r['Reaction_ID']} - Patient {r['Patient_ID']}") for r in reactions],
                format_func=lambda x: x[1]
            )
            if st.button("Delete Reaction"):
                delete_record("Reactions", "Reaction_ID", reaction_to_delete[0])

# def view_trial_details(trial_id):
#     # Make API call to get trial information
#     response = requests.get(f'http://localhost:5000/api/trial_information/{trial_id}')
#     if response.status_code == 200:
#         data = response.json()['data']
#         if data:
#             trial = data[0]  # Get the first (and should be only) trial
#             
#             st.subheader("Trial Details")
#             st.write(f"Name: {trial['Trial_Name']}")
#             st.write(f"Description: {trial['Description']}")
#             st.write(f"Duration: {trial['Trial_Start_Date']} to {trial['Trial_End_Date']}")
#             
#             st.subheader("Patient Information")
#             st.write(f"Name: {trial['Patient_First_Name']} {trial['Patient_Last_Name']}")
#             
#             st.subheader("Doctor Information")
#             st.write(f"Name: {trial['Doctor_First_Name']} {trial['Doctor_Last_Name']}")
#             st.write(f"Specialization: {trial['Specialization']}")
#             
#             st.subheader("Medication Information")
#             st.write(f"Name: {trial['Medication_Name']}")
#             st.write(f"Dosage: {trial['Dosage']}")
#             st.write(f"Administration Method: {trial['Administration_Method']}")
#             
#             if trial['Result_ID']:
#                 st.subheader("Results")
#                 st.write(f"Date: {trial['Result_Date']}")
#                 st.write(f"Details: {trial['Result_Details']}")
#                 st.write(f"Laboratory: {trial['Lab_Name']}")

# Update the main() function to include the new pages
def main():
    st.set_page_config(page_title="Medical Database Management", layout="wide")

    sidebar_nav()

    if st.session_state.current_page == 'Home':
        st.title("Medical Database Management System")
        st.write("""
        Welcome to the Medical Database Management System.
        Use the sidebar to navigate through different sections.
        """)

        # Display summary statistics
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
