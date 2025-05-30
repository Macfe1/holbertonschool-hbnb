# Implementation of Business Logic and API Endpoints

In this part of the HBnB Project, we will begin the implementation phase of the application based onthe design developed in the architecture part. The focus of this phase is to build the Presentation and Business Logic layers of the application using Python and Flask. We will use the facade pattern to communicate the presentation layer with the business loic layer.

## Project Directory Structure

 - The `app/` directory contains the core application code.
 - The `api/` subdirectory houses the API endpoints, organized by version (`v1/`).
 - The `models/` subdirectory contains the business logic classes (e.g., `user.py`, `place.py`).
 - The `services/` subdirectory is where the Facade pattern is implemented, managing the interaction between layers.
 - The `persistence/` subdirectory is where the in-memory repository is implemented. This will later be replaced by a database-backed solution using SQL Alchemy.
 - `run.py` is the entry point for running the Flask application.
 - `config.py` will be used for configuring environment variables and application settings.
 - `requirements.txt` will list all the Python packages needed for the project.
 - `README.md` will contain a brief overview of the project.

## Install the dependencies using:

```text
pip install -r requirements.txt
```
