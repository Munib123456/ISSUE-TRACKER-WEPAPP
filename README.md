# Learner Issue Tracker

KV6013 Final Year Project  
Munib Ahmed (23020140)  
Northumbria University 2025/26  
Supervisor: Victor Ayodele

## Overview

A Flask-based web application for managing student learning issues at course level. Lecturers create tracker boards, students raise issues, tutors are auto-added, and a TF-IDF duplicate detection module suggests joining existing similar issues to reduce duplication. Includes real-time chat per issue using WebSockets and content moderation through OpenRouter.

## Tech stack

- Flask + Jinja2
- SQLite
- Flask-Login (authentication)
- Flask-SocketIO (real-time chat)
- scikit-learn (TF-IDF duplicate detection)
- Bootstrap 5
- OpenRouter API (content moderation)

## How to run

1. Create a virtual environment:
python3 -m venv venv

2. Activate it:
   - Mac/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

3. Install dependencies:
pip install -r requirements.txt

4. Create a `.env` file in the project root with your OpenRouter API key:
OPENROUTER_API_KEY=your_key_here
SECRET_KEY=any_random_string
   (Note: content moderation will not work without this, but the rest of the app will run fine.)

5. Initialise the database:
python3 init_db.py

6. Run the application:
python3 run.py

7. Open in browser: http://localhost:5000

## Test accounts (seeded by init_db.py)

| Role     | Email              | Password    |
|----------|--------------------|-------------|
| Lecturer | lecturer@test.com  | password123 |
| Tutor    | tutor@test.com     | password123 |
| Student  | student@test.com   | password123 |

## Project structure
learner-issue-tracker/
├── app/
│   ├── routes/        # Flask Blueprints (auth, boards, issues, chat, main)
│   ├── models/        # Database models and helpers
│   ├── templates/     # Jinja2 HTML templates
│   ├── static/        # CSS and JavaScript
│   └── utils/         # Decorators, moderation logic
├── schema.sql         # Database schema
├── init_db.py         # Database initialiser with seeded accounts
├── run.py             # Application entry point
└── requirements.txt   # Python dependencies

## Notes

- Database is SQLite (`tracker.db`) which will be created when you run `init_db.py`.
- All passwords are hashed using werkzeug.security.
- Lecturers and tutors are seeded by the institution rather than self-registered, mirroring institutional tools like Turnitin or Blackboard.