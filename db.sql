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


SET @have_roles = (SELECT IF(COUNT(*) > 0, 'YES', 'NO') 
                   FROM information_schema.plugins 
                   WHERE PLUGIN_NAME = 'authentication_policy');

-- Create roles if supported
SET @create_role_stmt = IF(@have_roles = 'YES',
    'CREATE ROLE IF NOT EXISTS admin_role, doctor_role, lab_technician_role, research_assistant_role',
    'SELECT "Roles not supported in this MySQL version - using direct grants instead"');
PREPARE stmt FROM @create_role_stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Create users (if they don't exist)
CREATE USER IF NOT EXISTS 'admin_user' IDENTIFIED BY 'StrongAdminPass123!';
CREATE USER IF NOT EXISTS 'doctor_user' IDENTIFIED BY 'StrongDoctorPass123!';
CREATE USER IF NOT EXISTS 'lab_user' IDENTIFIED BY 'StrongLabPass123!';
CREATE USER IF NOT EXISTS 'research_user' IDENTIFIED BY 'StrongResearchPass123!';

-- Admin user permissions
GRANT ALL PRIVILEGES ON proj.* TO "admin_user";

-- Doctor user permissions
GRANT SELECT ON proj.* TO "doctor_user";
GRANT INSERT, UPDATE ON proj.Visit TO "doctor_user";
GRANT INSERT, UPDATE ON proj.Clinical_Trial TO "doctor_user";
GRANT INSERT ON proj.Reactions TO "doctor_user";

-- Lab user permissions
GRANT SELECT ON proj.* TO "lab_user";
GRANT INSERT, UPDATE ON proj.Results TO "lab_user";

-- Research user permissions
GRANT SELECT ON proj.* TO "research_user";
GRANT INSERT, UPDATE ON proj.Clinical_Trial TO "research_user";

-- Create view for sensitive patient information
CREATE OR REPLACE VIEW patient_basic_info AS
SELECT 
    Patient_ID,
    First_Name,
    Last_Name,
    Age,
    Gender,
    Last_Visit_ID
FROM Patient;

-- Grant view access
GRANT SELECT ON proj.patient_basic_info TO 'research_user';

-- Flush privileges to ensure all changes take effect
FLUSH PRIVILEGES;
