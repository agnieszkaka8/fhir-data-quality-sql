# FHIR Data Quality SQL Project

This project demonstrates how healthcare data based on the **HL7 FHIR standard** can be modeled in **PostgreSQL** and validated using **SQL-based data quality checks**.

## Project Structure

- `schema/` SQL scripts for creating database tables (FHIR resources)
- `data/` sample synthetic data
- `tests/` data quality checks in SQL
- `analytics/` clinical queries and aggregations

Synthetic healthcare data is generated using the Faker library with a fixed random seed to ensure reproducibility.

## Goal

- Understand FHIR resources
- Model them in SQL
- Detect common data quality issues