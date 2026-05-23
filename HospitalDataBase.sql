CREATE DATABASE HospitalDatabase;
USE HospitalDatabase;

-- Patients table
CREATE TABLE Patients (
    patient_id INT PRIMARY KEY,
    patient_name VARCHAR(100),
    province VARCHAR(50)
);

-- Treatments table
CREATE TABLE Treatments (
    treatment_id INT PRIMARY KEY,
    patient_id INT,
    treatment_name VARCHAR(100),
    category VARCHAR(50),
    unit_cost DECIMAL(10,2),
    quantity INT,
    treatment_date DATE,
    total_cost AS (unit_cost * quantity),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);

-- Sample data
INSERT INTO Patients VALUES
(1, 'Lindiwe Nkosi', 'Gauteng'),
(2, 'Pieter van Zyl', 'Western Cape'),
(3, 'Thabo Dlamini', 'KwaZulu-Natal'),
(4, 'Nomsa Khumalo', 'Eastern Cape');