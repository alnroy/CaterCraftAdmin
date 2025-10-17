🛠️ CaterCraft Admin — Admin Management System

A Django-based admin dashboard for the CaterCraft catering service application. This system allows admins to monitor and manage users, services, bookings, staff, and financial details from a single, secure interface.

✨ Key Features

🔑 Admin Authentication

Secure login for administrators

Role-based access (admin-only dashboard)

👥 User Management

View, edit, and delete customer and staff accounts

Monitor user activity and service interactions

Search and filter users efficiently

📋 Service & Booking Management

Track service bookings made by customers

Approve or reject service requests

Monitor completion status and service history

👨‍💼 Staff Management

Add, edit, and remove staff members

Assign staff to teams

Track staff performance and wages

💬 Communication & Feedback

View customer and staff feedback

🧩 Dashboard & Analytics

Visual insights for bookings, staff activity, and earnings

Key metrics at a glance

Real-time updates for operational efficiency

🏗️ Architecture & Tech Stack

Backend: Django (Python 3.13)

Frontend: django templates

Database: SQLite (default) 

Email notifications: Configurable via SMTP

Authentication: Django auth system

🚀 Getting Started
Prerequisites

Python 3.13+

Django

Virtual environment recommended

Installation

Clone the repository:

git clone https://github.com/<username>/CaterCraft-Admin.git
cd CaterCraft-Admin


Create and activate a virtual environment:

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py migrate


Create a superuser (admin):

python manage.py createsuperuser


Run the server:

python manage.py runserver


Open http://127.0.0.1:8000 in your browser to access the admin panel.

🔐 Security & Best Practices

Use strong passwords for admin accounts

Keep .env files or credentials out of GitHub

Enable HTTPS in production

Regularly update Django and dependencies

📝 Contributing

Fork the repository

Create a feature branch

Make changes & test

Open a pull request

🧑‍💻 Developer

Alan Roy – Developed with ❤️ for catering management
