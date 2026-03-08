-- Table: patients
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('male', 'female', 'other')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: practitioners
CREATE TABLE practitioners (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(100)
);

-- Table: encounters
CREATE TABLE encounters (
    id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patients(id),
    practitioner_id INT REFERENCES practitioners(id),
    encounter_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    encounter_type VARCHAR(50),
    notes TEXT
);

-- Table: observations
CREATE TABLE observations (
    id SERIAL PRIMARY KEY,
    encounter_id INT REFERENCES encounters(id),
    observation_name VARCHAR(100) NOT NULL,
    observation_type VARCHAR(100) NOT NULL,
    value NUMERIC,
    unit VARCHAR(50),
    observation_date DATE NOT NULL
);

-- Table: medication_requests
CREATE TABLE medication_requests (
    id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patients(id),
    practitioner_id INT NOT NULL REFERENCES practitioners(id),
    encounter_id INT REFERENCES encounters(id),
    medication_code VARCHAR(100) NOT NULL,
    dosage TEXT,
    status VARCHAR(50) NOT NULL CHECK (status IN ('requested', 'approved', 'denied')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
