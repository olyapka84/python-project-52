# Hexlet Tests and SonarCloud
[![Actions Status](https://github.com/olyapka84/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/olyapka84/python-project-52/actions)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=olyapka84_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=olyapka84_python-project-52)

# Task Manager

Task Manager is a web application built with Django that allows users to register, log in, and manage tasks with statuses and labels.
It’s a simple but fully functional project management tool created as the final project of the Hexlet Python Developer course.

---

## Demo

Deployed on Render:  
https://python-project-52-76f1.onrender.com/

---

## Features

- User registration and authentication  
- CRUD operations for:
  - Tasks (title, description, status, author, executor)
  - Statuses (e.g. "New", "In progress", "Done")
  - Labels for flexible task categorization  
- Access control: users can edit or delete only their own tasks  
- Flash messages for user feedback (success/error notifications)  
- Deployed with PostgreSQL and environment variables on Render  

---

## Tech Stack

- Backend: Django 5.x  
- Database: PostgreSQL  
- Frontend: Django Templates, Bootstrap  
- Testing: pytest
- Code quality: SonarCloud  

---

## Local Setup

Clone the repository and install dependencies with uv:

- git clone https://github.com/olyapka84/python-project-52.git
- cd python-project-52
- uv sync

Create a .env file in the project root:

DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/task_manager

Run database migrations:

- make migrate

Start the development server:

- make start

or directly:

- uv run python manage.py runserver 0.0.0.0:8000

Then open the app at:  
http://localhost:8000/

---

## Testing

Run the full test suite:

- make test

---

## About

This project was developed as part of the Hexlet Python Developer program.
- Author: Olga Akukina (https://github.com/olyapka84)
- Hexlet: https://hexlet.io
