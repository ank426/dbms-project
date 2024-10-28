import streamlit as st
import requests

# API URL
API_URL = "http://127.0.0.1:5000"

# Main Streamlit app
def main():
    st.title("Patient Management System")

    menu = ["Add Patient", "View Patients", "Delete Patient",
            "Add Doctor", "View Doctors", "Delete Doctor",
            "Add Visit", "View Visits", "Delete Visit"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Patient":
        st.subheader("Add New Patient")

        # Input fields for patient details
        patient_id = st.number_input("Patient ID", min_value=1, step=1)
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        dob = st.date_input("Date of Birth")
        contact = st.text_input("Contact Number")
        email = st.text_input("Email")
        address = st.text_area("Address")
        visit_id = st.number_input("Visit ID", min_value=1, step=1)
        medical_history = st.text_area("Medical History")

        if st.button("Add Patient"):
            patient_data = {
                "Patient_ID": patient_id,
                "First_Name": first_name,
                "Last_Name": last_name,
                "Gender": gender,
                "Date_of_Birth": str(dob),
                "Contact_Number": contact,
                "Email": email,
                "Address": address,
                "Visit_ID": visit_id,
                "Medical_History": medical_history
            }
            response = requests.post(f"{API_URL}/add_patient", json=patient_data)
            result = response.json()
            if result['status'] == 'success':
                st.success(result['message'])
            else:
                st.error(result['message'])

    elif choice == "View Patients":
        st.subheader("Patient List")
        response = requests.get(f"{API_URL}/patients")
        result = response.json()
        if result['status'] == 'success':
            patients = result['data']
            if patients:
                for patient in patients:
                    st.write(f"""
                        Patient ID: {patient['Patient_ID']}\n
                        Name: {patient['First_Name']} {patient['Last_Name']}\n
                        Gender: {patient['Gender']}\n
                        Date of Birth: {patient['Date_of_Birth']}\n
                    """)
            else:
                st.write("No patients found.")
        else:
            st.error(result['message'])

    elif choice == "Delete Patient":
        st.subheader("Delete Patient")
        patient_id = st.number_input("Enter Patient ID to delete", min_value=1, step=1)
        if st.button("Delete Patient"):
            response = requests.delete(f"{API_URL}/delete_patient", json={"Patient_ID": patient_id})
            result = response.json()
            if result['status'] == 'success':
                st.success(result['message'])
            else:
                st.error(result['message'])

# Doctor Management
    elif choice == "Add Doctor":
        st.subheader("Add New Doctor")

        # Input fields for doctor details
        doctor_id = st.number_input("Doctor ID", min_value=1, step=1)
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        specialization = st.text_input("Specialization")
        contact = st.text_input("Contact Number")
        email = st.text_input("Email")

        if st.button("Add Doctor"):
            doctor_data = {
                "Doctor_ID": doctor_id,
                "First_Name": first_name,
                "Last_Name": last_name,
                "Specialization": specialization,
                "Contact_Number": contact,
                "Email": email
            }
            response = requests.post(f"{API_URL}/add_doctor", json=doctor_data)
            result = response.json()
            if result['status'] == 'success':
                st.success(result['message'])
            else:
                st.error(result['message'])

    elif choice == "View Doctors":
        st.subheader("Doctor List")
        response = requests.get(f"{API_URL}/doctors")
        result = response.json()
        if result['status'] == 'success':
            doctors = result['data']
            if doctors:
                for doctor in doctors:
                    st.write(f"""
                        Doctor ID: {doctor['Doctor_ID']}\n
                        Name: {doctor['First_Name']} {doctor['Last_Name']}\n
                        Specialization: {doctor['Specialization']}\n
                    """)
            else:
                st.write("No doctors found.")
        else:
            st.error(result['message'])

    elif choice == "Delete Doctor":
        st.subheader("Delete Doctor")
        doctor_id = st.number_input("Enter Doctor ID to delete", min_value=1, step=1)
        if st.button("Delete Doctor"):
            response = requests.delete(f"{API_URL}/delete_doctor", json={"Doctor_ID": doctor_id})
            result = response.json()
            if result['status'] == 'success':
                st.success(result['message'])
            else:
                st.error(result['message'])

    # Visit Management
    elif choice == "Add Visit":
        st.subheader("Add New Visit")

        # Input fields for visit details
        visit_id = st.number_input("Visit ID", min_value=1, step=1)
        patient_id = st.number_input("Patient ID", min_value=1, step=1)
        doctor_id = st.number_input("Doctor ID", min_value=1, step=1)
        visit_date = st.date_input("Visit Date")
        visit_details = st.text_area("Visit Details")

        if st.button("Add Visit"):
            visit_data = {
                "Visit_ID": visit_id,
                "Patient_ID": patient_id,
                "Doctor_ID": doctor_id,
                "Visit_Date": str(visit_date),
                "Visit_Details": visit_details
            }
            response = requests.post(f"{API_URL}/add_visit", json=visit_data)
            result = response.json()
            if result['status'] == 'success':
                st.success(result['message'])
            else:
                st.error(result['message'])

    elif choice == "View Visits":
        st.subheader("Visit List")
        response = requests.get(f"{API_URL}/visits")
        result = response.json()
        if result['status'] == 'success':
            visits = result['data']
            if visits:
                for visit in visits:
                    st.write(f"""
                        Visit ID: {visit['Visit_ID']}\n
                        Patient ID: {visit['Patient_ID']}\n
                        Doctor ID: {visit['Doctor_ID']}\n
                        Visit Date: {visit['Visit_Date']}\n
                        Details: {visit['Visit_Details']}\n
                    """)
            else:
                st.write("No visits found.")
        else:
            st.error(result['message'])

    elif choice == "Delete Visit":
        st.subheader("Delete Visit")
        visit_id = st.number_input("Enter Visit ID to delete", min_value=1, step=1)
        if st.button("Delete Visit"):
            response = requests.delete(f"{API_URL}/delete_visit", json={"Visit_ID": visit_id})
            result = response.json()
            if result['status'] == 'success':
                st.success(result['message'])
            else:
                st.error(result['message'])

if __name__ == "__main__":
    main()

