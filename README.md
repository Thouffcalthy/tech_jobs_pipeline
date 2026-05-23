**Read this in other lannguage**

# Tech Job Market Data Pipeline (Work in Progress)

This project is a hands-on data engineering exercise focused on designing and implementing a structured ingestion pipeline for job market data.

The initial focus is on building a solid PostgreSQL schema before implementing the full extraction and transformation pipeline. The goal is to understand how data from different external sources can be normalized, validated, and stored in a consistent structure.

At this stage, the relational schema is implemented and includes integrity constraints, controlled categorical attributes, and explicit many-to-many relationships. The ingestion logic is currently under development.

---

## Architecture Direction

The intended workflow follows a batch-oriented approach:

Public APIs --> Extraction --> Transformation --> PostgreSQL

The extraction layer will be responsible for integrating with different APIs, handling pagination, tracking data sources, and preventing duplicate ingestion using composite identifiers.

The transformation step will standardize experience levels, salary ranges, and work modes, while cleaning inconsistent fields. Loading will be controlled to preserve referential integrity and enforce database-level constraints.

---

## Data Model

The schema is normalized and centered around the jobs table, which connects companies, locations, sources and skills.

Key characteristics of the model include:

- Use of GENERATED ALWAYS AS IDENTITY
- ENUM types for controlled attributes such as job mode and experience level.
- Composite uniqueness for external identifiers.
- Check constraints for salary validation.
- Conditional constraints for onsite and hybrid roles.
- Separation between raw and normalized experience fields.
- A bridge table (jobs_skills) to manage many-to-many relationships.

Business logic is partially enforced at the database level to reduce downstream data cleaning and improve analytical reliability.

---

## Current Status

- Relational schema completed 
- Integrity constraints implemented
- Extraction and transformation logic in progress

The design is expected to evolve as the ingestion layer matures.

---

## Development Approach

This repository is built incrementally, prioritizing clarity and data integrity over rapid feature expansion. Refactoring is considered part of the process as new requirements emerge.


