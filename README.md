# FunChat -- CS50 Final Project

#### Video Demo: https://youtu.be/l3V7b5KAXqE

#### Description:

FunChat is a web-based chatting application built with Python and Flask as my final project for CS50x - Introduction to Computer Science. I wanted to build a web application where people can sign up for, log in to, and use to send messages to each other in a common chat room. The project helped me to understand how the web applications actually work.

## Why I Built This

Before building this project or studying this cousre I had no idea the these systems work, like how backend and frontend communicates with each other. Back then I didn't knew what happens when i click the "Sign Up" or "Send" or "Log In" buttons. Building FunChat helped me understand from the scratch how this system works.

## Features

- **User Registration & Login** -- Users can create an account with a username,
  email, and password. Passwords are hashed using Werkzeug before being stored
  in the database. No plain-text passwords are ever saved.
- **Shared Chat Room** -- All logged-in users can send messages that appear in
  a shared chat room visible to everyone.
- **Edit Messages** -- Users can edit their own messages after sending them.
- **Delete Messages** -- Users can delete their own messages from the chat room.
- **User Profile Page** -- Each user has a profile page showing their account details.
- **Forgot Password** -- A basic password recovery flow is included.
- **Login Required** -- Protected pages redirect unauthenticated users to the login page.

## Project Structure and File Explanations

```
Chat-App/
│── app.py              # Main Flask app
│── helpers.py          # login_required function
│── database.db         # Database file
│
├── static/             # CSS and other files
│
└── templates/          # HTML files
    │── layout.html
    │── index.html
    │── login.html
    │── register.html
    │── edit.html
    │── profile.html
    └── forgot.html
```

**app.py** -- This is the main part of this application. It contains all the flask routes that handles every page and actionn in the application. This inlcude the register route that handles user input and insert new users into the database, the login route that check the credentials and starts a session, the index route that loads and displays all messages, the edit route and delete routes that alllow the user to edit or delete their own messages after sending, the profile route that fetches the display the user data, and the logout route that clears the session. 

**helpers.py** -- This file contains the `login_required` decorator funciton. Its job is to protect certain routes so that only logged-in users can access them. If any unauthenticated user tries to visit a protect page, then he or shee will be redirected to login page.  separated this into its own file to keep `app.py` clean and to follow the principle of separating concerns -- the same pattern used in CS50's Finance problem set.

**database.db** -- This is the SQLite database file that stores all application data.
It contains two tables: `users`, which stores account information including hashed
passwords and registration timestamps, and `messages`, which stores every chat message
along with the user ID of who sent it and when.

**static/** -- This folder contains the CSS stylesheet that controls the visual design
of the application -- the layout, colors, navbar styling, message box appearance,
and responsive behavior.

**templates/** -- This folder contains all the HTML files rendered by Flask using the
Jinja2 templating engine.

- `layout.html` -- The base template. Every other page extends this file. It contains
  the navbar and the overall page structure so I don't have to repeat HTML across
  every template.
- `index.html` -- The main chat room page. Displays all messages and includes the
  form to send a new message.
- `login.html` -- The login form.
- `register.html` -- The registration form with fields for username, email, and password.
- `edit.html` -- A form that lets a user edit one of their existing messages.
- `profile.html` -- Displays the logged-in user's account details.
- `forgot.html` -- A basic password recovery page.

## What I learned

I chose Flask and SQLite because they are simple and helped me understand how everything works step by step. The hardest part was building routes for editing and deleting messages with proper checks. I also used AI for about 25% of the CSS to fix design issues. This project really helped me understand backend basics and sessions.

## Tech Stack

- Python 3
- Flask
- Flask-Session
- SQLite (via cs50 library)
- Werkzeug (password hashing)
- HTML & CSS
- Jinja2

## How to Run

1. Clone the repository
   `git clone https://github.com/adityaraj-devx/Chat-App.git`
   `cd Chat-App`

2. Install dependencies
   `pip install flask flask-session cs50 werkzeug`

3. Create Database

    ```Run this in Python:

    from cs50 import SQL
    db = SQL("sqlite:///database.db")

    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL,
        created_at TEXT
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    ```

4. Run the app
   `python app.py`

Then open your browser and go to `http://127.0.0.1:5000`