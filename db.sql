CREATE TABLE Patient (
    Patient_ID INT PRIMARY KEY,
    First_Name VARCHAR(100),
    Last_Name VARCHAR(100),
    Gender VARCHAR(10),
    Date_of_Birth DATE,
    Contact_Number VARCHAR(15),
    Email VARCHAR(100),
    Address VARCHAR(255),
    Last_Visit_ID INT,
    Medical_History VARCHAR(255)
);

CREATE TABLE Laboratory (
    Lab_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Location VARCHAR(255),
    Contact_Number VARCHAR(15),
    Email VARCHAR(100)
);

CREATE TABLE Doctor (
    Doctor_ID INT PRIMARY KEY,
    First_Name VARCHAR(100),
    Last_Name VARCHAR(100),
    Specialization VARCHAR(100),
    Contact_Number VARCHAR(15),
    Email VARCHAR(100),
    Lab_ID INT,
    FOREIGN KEY (Lab_ID) REFERENCES Laboratory(Lab_ID)
);
CREATE TABLE Visit (
    Visit_ID INT PRIMARY KEY,
    Patient_ID INT,
    Doctor_ID INT,
    Visit_Date DATE,
    Visit_Details VARCHAR(255),
    Prescription_ID INT,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor(Doctor_ID),
);

DELIMITER $$

CREATE TRIGGER UpdateLastVisitID
AFTER INSERT ON Visit
FOR EACH ROW
BEGIN
    UPDATE Patient
    SET Last_Visit_ID = NEW.Visit_ID
    WHERE Patient_ID = NEW.Patient_ID;
END $$

DELIMITER ;

CREATE TABLE Manufacturer (
    Manufacturer_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Contact_Number VARCHAR(15),
    Address VARCHAR(255)
);

CREATE TABLE Medication (
    Medication_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Manufacturer_ID INT,
    Dosage VARCHAR(50),
    Side_Effects VARCHAR(255),
    Frequency VARCHAR(50),
    Administration_Method VARCHAR(50),
    FOREIGN KEY (Manufacturer_ID) REFERENCES Manufacturer(Manufacturer_ID)
);


CREATE TABLE Clinical_Trial (
    Trial_ID INT PRIMARY KEY,
    Trial_Name VARCHAR(255),
    Description TEXT,
    Trial_Start_Date DATE,
    Trial_End_Date DATE,
    Patient_ID INT,
    Medication_ID INT,
    Doctor_ID INT,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Medication_ID) REFERENCES Medication(Medication_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor(Doctor_ID)
);

CREATE TABLE Results (
    Result_ID INT PRIMARY KEY,
    Trial_ID INT,
    Lab_ID INT,
    Patient_ID INT,
    Result_Date DATE,
    Result_Details TEXT,
    FOREIGN KEY (Trial_ID) REFERENCES Clinical_Trial(Trial_ID),
    FOREIGN KEY (Lab_ID) REFERENCES Laboratory(Lab_ID),
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID)
);

CREATE TABLE Reactions (
    Reaction_ID INT PRIMARY KEY,
    Patient_ID INT,
    Medication_ID INT,
    Reaction_Details TEXT,
    Date_of_Reaction DATE,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Medication_ID) REFERENCES Medication(Medication_ID)
);
