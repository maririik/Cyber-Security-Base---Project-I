# Cybersecurity Project - Notes App

A simple Django notes application created for the Cyber Security Base 2025 course.
The application contains 5 intentional security flaws from the OWASP Top 10 2021 list.

## Setup

pip install django
python manage.py makemigrations notes_app
python manage.py migrate
python manage.py runserver

Then go to http://localhost:8000/register/ to create an account.

## Flaws

1. A03 Injection - SQL injection in search
2. A01 Broken Access Control - users can view other users notes
3. A02 Cryptographic Failures - passwords stored in plaintext
4. A05 Security Misconfiguration - DEBUG=True and hardcoded secret key
5. A07 Identification and Authentication Failures - no password requirements