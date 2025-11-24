 vitatracker-
 VitaTracker is a web application designed to help users track daily vitamin intake, manage medication schedules, and monitor health adherence. It provides features like user authentication, personalized vitamin management, scheduling, and detailed intake reports built with Python, Flask, and MySQL.
 
VitaTracker – Vitamin Intake Tracking System
VitaTracker is a comprehensive web application designed to help users track their daily vitamin intake, manage medication schedules, and monitor adherence to their health regimens. By providing real-time tracking and detailed history reports, VitaTracker ensures you never miss a dose.
________________________________________
📋 Table of Contents
•	Overview
•	Features
•	Technology Stack
•	Project Structure
•	Installation & Setup
•	Configuration
•	Usage & Testing Guide
•	Database Schema
•	Future Enhancements
•	Screenshots
________________________________________
🌟 Features
=> User Authentication
•	Secure registration and login system.
•	Password hashing using Werkzeug security.
•	Session-based authentication for data privacy.
=> Vitamin Management (CRUD)
•	Create: Add vitamins with name, dosage, frequency, and custom notes.
•	Read: View a clean table of all tracked supplements.
•	Update: Edit details for existing vitamins.
•	Delete: Remove vitamins from your list.
=> Schedule Management
•	Create custom schedules for specific times of the day.
•	Set recurrence for specific days of the week or daily.
•	Visual dashboard of today's required intake.
=> Daily Intake Logging
•	Dashboard: Real-time view of "Today's Vitamins."
•	Quick Actions: Mark items as Taken or Missed with a single click.
•	Visual Feedback: Immediate status updates on the UI.
•History & Reports
•	History Log: Filterable list of all past intakes.
•	Analytics: Statistics on adherence percentage, total taken, and total missed.
•	30-Day Breakdown: Visual insight into recent activity.
________________________________________
=> Technology Stack
Component	Technology
Backend	Python 3, Flask
Database	MySQL 8.0+
Frontend	HTML5, CSS3, Jinja2 Templates
Security	Werkzeug (Hashing)
Session Mgmt	Flask Sessions
________________________________________
=> Project Structure
code Text
downloadcontent_copy
expand_less
---text
    VitaTracker/
│
├── app.py                 # Main application entry point
├── config.py              # Configuration variables
├── requirements.txt       # Python dependencies
├── schema.sql             # Database creation script
│
├── models/
│   └── db.py             # Database connection logic
│
├── routes/
│   ├── auth.py           # Login/Register routes
│   ├── vitamins.py       # Vitamin CRUD operations
│   ├── schedule.py       # Schedule management
│   └── logs.py           # Intake logic and reporting
│
├── templates/            # HTML files
│   ├── base.html         # Layout template
│   ├── dashboard.html    # Main user hub
│   ├── ... (other html files)
│
└── static/
    └── css/
        └── style.css     # Custom styling
  ---
________________________________________
=>Installation & Setup
Follow these steps to get the project running on your local machine.
Prerequisites
•	Python 3.8 or higher
•	MySQL Server 8.0 or higher
•	pip (Python package installer)
Step 1: Clone the Repository
code Bash
downloadcontent_copy
expand_less
    git  clone https://github.com/Hansini2325/vitatracker-
cd VitaTracker
  
Step 2: Install Dependencies
It is recommended to use a virtual environment.
code Bash
downloadcontent_copy
expand_less
    # Create virtual environment (Optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
  
Step 3: Database Setup
1.	Start your MySQL Server.
2.	Run the schema script to create the database and tables.
code Bash
downloadcontent_copy
expand_less
    # Run this in your terminal
mysql -u root -p < schema.sql
  
Step 4: Configuration
Edit the config.py file or set the following environment variables in your terminal to match your local database credentials:
Windows (PowerShell):
code Powershell
downloadcontent_copy
expand_less
    $env:MYSQL_HOST="localhost"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="your_password"
$env:MYSQL_DB="vitatracker"
$env:SECRET_KEY="your-super-secret-key"
  
Mac/Linux:
code Bash
downloadcontent_copy
expand_less
    export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DB=vitatracker
export SECRET_KEY=your-super-secret-key
  
Step 5: Run the Application
code Bash
downloadcontent_copy
expand_less
    python app.py
  
Open your browser and navigate to: http://localhost:5000
________________________________________
=> Usage & Testing Guide
To test the full functionality of the application, follow this flow:
1. Authentication
•	Go to /register and create a new user account.
•	Log in via /login. You should be redirected to the Dashboard.
2. Populating Data
•	Navigate to Vitamins -> Add Vitamin.
o	Test: Add "Vitamin C", Dose "500mg", Frequency "Daily".
•	Navigate to Schedule -> Add Schedule.
o	Test: Select "Vitamin C", choose a Time (e.g., 08:00 AM), and save.
3. Simulating Daily Usage
•	Go to the Dashboard. You should see "Vitamin C" listed for today.
•	Click "Mark Taken". The status should change immediately.
•	Test Edge Case: Add another schedule for a different time, return to dashboard, and click "Mark Missed".
4. Viewing Analytics
•	Navigate to History to see the raw logs of your actions.
•	Navigate to Report to view your Adherence Percentage (e.g., 50% if you took 1 and missed 1).
________________________________________
=> Database Schema Overview
The application uses a relational database with the following key tables:
1.	Users: Stores id, username, email, and password_hash.
2.	Vitamins: Stores vitamin_details linked to user_id.
3.	Schedules: Maps vitamins to specific times and days.
4.	Intake Logs: Records the status (taken/missed) and timestamp.
________________________________________
=> Future Enhancements
Email or SMS notifications for scheduled times.
Mobile-responsive UI improvements.
Export data to PDF/CSV for doctor visits.
Drug interaction warnings.
________________________________________
=> Screenshots
<img width="1916" height="991" alt="Dashboard" src="https://github.com/user-attachments/assets/d92c93f0-5125-44e4-b9b6-83e2b95d8472" />

________________________________________

Author : Burra Hansini 

