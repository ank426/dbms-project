CREATE TABLE Patient (
    Patient_ID INT PRIMARY KEY,
    First_Name VARCHAR(100) NOT NULL CHECK (First_Name <> ''),
    Last_Name VARCHAR(100) NOT NULL CHECK (Last_Name <> ''),
    Age INT CHECK (Age >= 18),
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
    Name VARCHAR(255) NOT NULL CHECK (Name <> ''),
    Location VARCHAR(255),
    Contact_Number VARCHAR(15),
    Email VARCHAR(100)
);

CREATE TABLE Doctor (
    Doctor_ID INT PRIMARY KEY,
    First_Name VARCHAR(100) NOT NULL CHECK (First_Name <> ''),
    Last_Name VARCHAR(100) NOT NULL CHECK (Last_Name <> ''),
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
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor(Doctor_ID)
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
    Name VARCHAR(100) NOT NULL CHECK (Name <> ''),
    Email VARCHAR(100),
    Contact_Number VARCHAR(15),
    Address VARCHAR(255)
);

CREATE TABLE Medication (
    Medication_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL CHECK (Name <> ''),
    Manufacturer_ID INT,
    Dosage VARCHAR(50),
    Side_Effects VARCHAR(255),
    Frequency VARCHAR(50),
    Administration_Method VARCHAR(50),
    FOREIGN KEY (Manufacturer_ID) REFERENCES Manufacturer(Manufacturer_ID)
);


CREATE TABLE Clinical_Trial (
    Trial_ID INT PRIMARY KEY,
    Trial_Name VARCHAR(255) NOT NULL CHECK (Trial_Name <> ''),
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

DELIMITER $$

CREATE PROCEDURE GetTrialInformation(IN trial_id_param INT)
BEGIN
    SELECT 
        ct.Trial_ID,
        ct.Trial_Name,
        ct.Description,
        ct.Trial_Start_Date,
        ct.Trial_End_Date,
        -- Patient Information
        p.Patient_ID,
        p.First_Name AS Patient_First_Name,
        p.Last_Name AS Patient_Last_Name,
        -- Doctor Information
        d.Doctor_ID,
        d.First_Name AS Doctor_First_Name,
        d.Last_Name AS Doctor_Last_Name,
        d.Specialization,
        -- Medication Information
        m.Medication_ID,
        m.Name AS Medication_Name,
        m.Dosage,
        m.Side_Effects,
        m.Administration_Method,
        -- Results Information
        r.Result_ID,
        r.Result_Date,
        r.Result_Details,
        -- Laboratory Information
        l.Lab_ID,
        l.Name AS Lab_Name
    FROM Clinical_Trial ct
    LEFT JOIN Patient p ON ct.Patient_ID = p.Patient_ID
    LEFT JOIN Doctor d ON ct.Doctor_ID = d.Doctor_ID
    LEFT JOIN Medication m ON ct.Medication_ID = m.Medication_ID
    LEFT JOIN Results r ON ct.Trial_ID = r.Trial_ID
    LEFT JOIN Laboratory l ON r.Lab_ID = l.Lab_ID
    WHERE ct.Trial_ID = trial_id_param;
END $$

DELIMITER ;
