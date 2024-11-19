-- Populating Patient table
INSERT INTO Patient (Patient_ID, First_Name, Last_Name, Age, Gender, Date_of_Birth, Contact_Number, Email, Address, Last_Visit_ID, Medical_History) VALUES
(1, 'John', 'Doe', 30, 'Male', '1993-01-01', '1234567890', 'john.doe@example.com', '123 Elm Street', NULL, 'No significant medical history'),
(2, 'Jane', 'Smith', 25, 'Female', '1998-02-02', '2345678901', 'jane.smith@example.com', '456 Oak Avenue', NULL, 'Asthma'),
(3, 'Alice', 'Johnson', 40, 'Female', '1983-03-03', '3456789012', 'alice.johnson@example.com', '789 Pine Road', NULL, 'Diabetes'),
(4, 'Bob', 'Brown', 35, 'Male', '1988-04-04', '4567890123', 'bob.brown@example.com', '321 Maple Blvd', NULL, 'Hypertension'),
(5, 'Charlie', 'Davis', 50, 'Male', '1973-05-05', '5678901234', 'charlie.davis@example.com', '654 Birch Lane', NULL, 'Heart Disease');

-- Populating Laboratory table
INSERT INTO Laboratory (Lab_ID, Name, Location, Contact_Number, Email) VALUES
(1, 'LabCorp', 'Downtown', '1234567890', 'contact@labcorp.com'),
(2, 'Quest Diagnostics', 'Uptown', '2345678901', 'info@questdiag.com'),
(3, 'BioLab', 'Midtown', '3456789012', 'support@biolab.com'),
(4, 'Pathology Associates', 'Northside', '4567890123', 'admin@pathology.com'),
(5, 'Genetics Lab', 'Eastside', '5678901234', 'genetics@genlab.com');

-- Populating Doctor table
INSERT INTO Doctor (Doctor_ID, First_Name, Last_Name, Specialization, Contact_Number, Email, Lab_ID) VALUES
(1, 'Emily', 'Clark', 'Cardiology', '1231231234', 'emily.clark@hospital.com', 1),
(2, 'Michael', 'Adams', 'Neurology', '2342342345', 'michael.adams@hospital.com', 2),
(3, 'Sarah', 'Miller', 'Oncology', '3453453456', 'sarah.miller@hospital.com', 3),
(4, 'Daniel', 'Jones', 'Pediatrics', '4564564567', 'daniel.jones@hospital.com', 4),
(5, 'Sophia', 'Wilson', 'Dermatology', '5675675678', 'sophia.wilson@hospital.com', 5);

-- Populating Visit table
INSERT INTO Visit (Visit_ID, Patient_ID, Doctor_ID, Visit_Date, Visit_Details) VALUES
(1, 1, 1, '2024-01-10', 'Routine check-up'),
(2, 2, 2, '2024-02-15', 'Follow-up for migraine treatment'),
(3, 3, 3, '2024-03-20', 'Consultation for cancer screening'),
(4, 4, 4, '2024-04-25', 'Child immunization'),
(5, 5, 5, '2024-05-30', 'Skin rash evaluation');

-- Populating Manufacturer table
INSERT INTO Manufacturer (Manufacturer_ID, Name, Email, Contact_Number, Address) VALUES
(1, 'PharmaCorp', 'contact@pharmacorp.com', '1231231231', '123 Industry Street'),
(2, 'GlobalMed', 'info@globalmed.com', '2342342342', '456 Science Avenue'),
(3, 'HealthPlus', 'support@healthplus.com', '3453453453', '789 Medical Road'),
(4, 'BioPharma', 'admin@biopharma.com', '4564564564', '321 Research Blvd'),
(5, 'MedLife', 'contact@medlife.com', '5675675675', '654 Pharmacy Lane');

-- Populating Medication table
INSERT INTO Medication (Medication_ID, Name, Manufacturer_ID, Dosage, Side_Effects, Frequency, Administration_Method) VALUES
(1, 'Aspirin', 1, '500mg', 'Nausea', 'Once daily', 'Oral'),
(2, 'Ibuprofen', 2, '200mg', 'Dizziness', 'Twice daily', 'Oral'),
(3, 'Metformin', 3, '1000mg', 'Stomach upset', 'Twice daily', 'Oral'),
(4, 'Lipitor', 4, '20mg', 'Muscle pain', 'Once daily', 'Oral'),
(5, 'Zoloft', 5, '50mg', 'Drowsiness', 'Once daily', 'Oral');

-- Populating Clinical_Trial table
INSERT INTO Clinical_Trial (Trial_ID, Trial_Name, Description, Trial_Start_Date, Trial_End_Date, Patient_ID, Medication_ID, Doctor_ID) VALUES
(1, 'Trial Alpha', 'Testing drug efficiency', '2024-01-01', '2024-06-01', 1, 1, 1),
(2, 'Trial Beta', 'New pain relief study', '2024-02-01', '2024-07-01', 2, 2, 2),
(3, 'Trial Gamma', 'Cancer medication trial', '2024-03-01', '2024-08-01', 3, 3, 3),
(4, 'Trial Delta', 'Diabetes treatment trial', '2024-04-01', '2024-09-01', 4, 4, 4),
(5, 'Trial Epsilon', 'Cholesterol medication test', '2024-05-01', '2024-10-01', 5, 5, 5);

-- Populating Results table
INSERT INTO Results (Result_ID, Trial_ID, Lab_ID, Patient_ID, Result_Date, Result_Details) VALUES
(1, 1, 1, 1, '2024-07-01', 'Positive outcome with minor side effects'),
(2, 2, 2, 2, '2024-08-01', 'Significant pain reduction'),
(3, 3, 3, 3, '2024-09-01', 'Tumor shrinkage observed'),
(4, 4, 4, 4, '2024-10-01', 'Improved blood sugar levels'),
(5, 5, 5, 5, '2024-11-01', 'Lower cholesterol levels achieved');

-- Populating Reactions table
INSERT INTO Reactions (Reaction_ID, Patient_ID, Medication_ID, Reaction_Details, Date_of_Reaction) VALUES
(1, 1, 1, 'Mild headache', '2024-01-15'),
(2, 2, 2, 'Upset stomach', '2024-02-20'),
(3, 3, 3, 'Fatigue', '2024-03-25'),
(4, 4, 4, 'Nausea', '2024-04-30'),
(5, 5, 5, 'Skin irritation', '2024-05-05');
