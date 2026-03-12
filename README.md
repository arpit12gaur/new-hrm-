
# HRMS Lite

## Overview
A lightweight HRMS system to manage employees and track attendance.

## Tech Stack
Frontend: HTML + Tailwind CSS + JavaScript  
Backend: FastAPI (Python)  
Database: SQLite  
ORM: SQLAlchemy

## Features
- Add employee
- View employees
- Delete employee
- Mark attendance
- View attendance history
- Email validation
- Duplicate employee prevention
- Loading and empty UI states

## Run Locally

Backend:

cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Open API docs:
http://localhost:8000/docs

Frontend:

Open frontend/index.html

## Assumptions
Single admin user. No authentication required.
