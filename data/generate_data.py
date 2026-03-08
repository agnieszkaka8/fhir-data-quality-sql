import random
from datetime import datetime, timedelta

import psycopg2
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# DATABASE CONFIGURATION

NUM_PATIENTS = 100
NUM_PRACTITIONERS = 20
NUM_ENCOUNTERS = 200
NUM_OBSERVATIONS = 400
NUM_MEDICATION_REQUESTS = 120

DB_CONFIG = {
    "dbname": "medical_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

SPECIALIZATIONS = [
    "cardiology",
    "dermatology",
    "neurology",
    "pediatrics",
    "radiology",
    "surgery",
    "psychiatry",
    "urology",
    "general practice"
]

OBSERVATION_TYPES = [
    ("heart_rate", "bpm", (60, 100)),
    ("blood_pressure_systolic", "mmHg", (100, 140)),
    ("blood_pressure_diastolic", "mmHg", (60, 90)),
    ("temperature", "°C", (36.5, 39)),
    ("oxygen_saturation", "%", (90, 100))
]

MEDICATION_CODES = [
    ("aspirin", "Aspirin", "oral", "100mg"),
    ("lisinopril", "Lisinopril", "oral", "20mg"),
    ("metformin", "Metformin", "oral", "500mg"),
    ("atorvastatin", "Atorvastatin", "oral", "10mg"),
    ("amoxicillin", "Amoxicillin", "oral", "250mg")
]

MEDICATION_STATUS = ["requested", "approved", "denied"]

GENDERS = ["male", "female", "other"]

# DB CONNECTION
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

cursor = get_db_connection().cursor()

# PREPARE PATIENT DATA

for _ in range(NUM_PATIENTS):
    first_name = fake.first_name()
    last_name = fake.last_name()
    birth_date = fake.date_of_birth(minimum_age=0, maximum_age=115)
    gender = random.choice(GENDERS)
    created_at = datetime.now() - timedelta(days=random.randint(0, 365 * 10))

    cursor.execute(
        """
        INSERT INTO patients (first_name, last_name, birth_date, gender, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, birth_date, gender, created_at)
        );

# GET PATIENT IDS

cursor.execute("SELECT id FROM patients")
patient_ids = [row[0] for row in cursor.fetchall()]

# PREPARE PRACTITIONER DATA

for _ in range(NUM_PRACTITIONERS):
    first_name = fake.first_name()
    last_name = fake.last_name()
    specialization = random.choice(SPECIALIZATIONS)

    cursor.execute(
        """
        INSERT INTO practitioners (first_name, last_name, specialization)
        VALUES (%s, %s, %s)
        """, (first_name, last_name, specialization)
    );

# GET PRACTITIONER IDS

cursor.execute("SELECT id FROM practitioners")
practitioners_ids = [row[0] for row in cursor.fetchall()]

# PREPARE ENCOUNTER DATA

for _ in range(NUM_ENCOUNTERS):
    encounter_id = fake.uuid4()
    patient_id = random.choice(patient_ids)
    practitioner_id = random.choice(practitioners_ids)
    encounter_date = datetime.now() - timedelta(days=random.randint(0, 365 * 5))
    encounter_type = random.choice(["office", "telehealth"])
    notes = fake.text()

    cursor.execute(
        """
        INSERT INTO encounters (patient_id, practitioner_id, encounter_date, encounter_type, notes)
        VALUES(%s, %s, %s, %s, %s)
        """, (patient_id, practitioner_id, encounter_date, encounter_type, notes)
    );

# GET ENCOUNTER IDS

cursor.execute("SELECT id FROM encounters")
encounter_ids = [row[0] for row in cursor.fetchall()]

# PREPARE OBSERVATION DATA

for _ in range(NUM_OBSERVATIONS):

    encounter_id = random.choice(encounter_ids)

    cursor.execute("SELECT encounter_date FROM encounters WHERE id = %s", (encounter_id,))
    encounter_date_real = cursor.fetchone()[0]

    obs_type, obs_unit, (low, high) = random.choice(OBSERVATION_TYPES)

    observation_name = obs_type
    value = round(random.uniform(low, high), 2)
    unit = obs_unit
    observation_date = encounter_date_real + timedelta(days=random.randint(0, 30))

    cursor.execute(
        """
        INSERT INTO observations (encounter_id, observation_name, value, unit, observation_date)
        VALUES (%s, %s, %s, %s, %s)
        """, (encounter_id, observation_name, value, unit, observation_date)
    );

# PREPARE MEDICATION DATA

for _ in range(NUM_MEDICATION_REQUESTS):

    encounter_id = random.choice(encounter_ids)

    cursor.execute("SELECT encounter_date FROM encounters WHERE id = %s", (encounter_id,))
    encounter_date_real = cursor.fetchone()[0]

    med_name, med_label, med_route, med_dose = random.choice(MEDICATION_CODES)

    medication_code = med_label
    dosage = med_dose
    status = random.choice(MEDICATION_STATUS)
    created_at = encounter_date_real + timedelta(days=random.randint(0, 30))

    cursor.execute(
        """
        INSERT INTO medication_requests (encounter_id, medication_code, dosage, status, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """, (encounter_id, medication_code, dosage, status, created_at)
    );

# COMMIT

conn.commit()
cursor.close()
conn.close()