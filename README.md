# Flask Vulnerable App

This is a Flask-based web application designed to demonstrate common web security vulnerabilities. The application includes features such as user authentication, session management, and a simple transfer functionality.

## Prerequisites
Make sure you have Python installed (Python 3.6 or later is recommended).

## Setting Up the Virtual Environment
1. Open a terminal or command prompt.
2. Navigate to the project directory:
   ```sh
   cd /path/to/project
   ```
3. Create a virtual environment:
   ```sh
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

## Installing Dependencies
After activating the virtual environment, install Flask using pip:
```sh
pip install flask
```

## Running the Server
1. Initialize the database and start the Flask server:
   ```sh
   python vuln_app.py
   ```
2. The server will start in debug mode and can be accessed at:
   ```
   http://127.0.0.1:5000/
   ```

## Project Structure
- `vuln_app.py` - Main Flask application file.
- `templates/` - HTML templates for the frontend.
- `database.db` - SQLite database file (automatically created and reset on each run).

## Features
- Basic user authentication with admin credentials.
- Transfer functionality between predefined accounts.
- Common web security vulnerabilities including XSS, session fixation, and CSRF.

## Notes
This application is intentionally vulnerable for educational purposes. **Do not deploy it in a production environment.**

## License
This project is licensed under the MIT License.

