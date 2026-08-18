# Copilot Instructions for Mergington High School API

## Running the Application

### Development Server
```bash
# Install dependencies (one-time setup)
pip install -r requirements.txt

# Start the development server with auto-reload
uvicorn src.app:app --reload

# The API will be available at http://localhost:8000
# Auto-generated API documentation: http://localhost:8000/docs
```

### Running Tests
```bash
# Run all tests
pytest

# Run tests in a specific file
pytest tests/test_activities.py

# Run tests with verbose output
pytest -v

# Run tests with coverage
pytest --cov=src
```

### Linting & Code Quality
The project uses Python with no pre-configured linter. Consider running standard checks:
```bash
# If available
pylint src/
black --check src/
```

## Project Architecture

### Overview
This is a FastAPI-based REST API for managing high school extracurricular activities. Students can view available activities and sign up for them.

### Key Components

**Backend Structure:**
- `src/app.py` - Main FastAPI application
  - In-memory activity database (global `activities` dict)
  - Three endpoints: root redirect, GET activities list, POST signup
  - Static file serving for frontend assets

**Frontend Structure:**
- `src/static/index.html` - Main HTML page
- `src/static/app.js` - Client-side logic for fetching activities and handling signups
- `src/static/styles.css` - Styling

**Data Model:**
The `activities` dictionary contains activity objects with this structure:
```python
{
  "Activity Name": {
    "description": str,
    "schedule": str,
    "max_participants": int,
    "participants": [list of emails]
  }
}
```

### API Endpoints

- `GET /` - Redirects to `/static/index.html`
- `GET /activities` - Returns all activities and their participants
- `POST /activities/{activity_name}/signup?email={email}` - Adds a student to an activity

## Key Conventions

### Participant Management
- Participants are stored as email addresses (e.g., `"student@mergington.edu"`)
- No capacity validation is enforced (despite the `max_participants` field)
- Duplicate signup attempts return a 400 error with "Student already signed up" message

### Error Handling
- Non-existent activities return HTTP 404
- Duplicate signups return HTTP 400
- Use `HTTPException` from FastAPI for all error responses

### Data Persistence
- All data is in-memory; restarting the server resets the database
- No database integration or persistence layer exists

## Development Environment

- **Python Version:** 3.13 (via devcontainer)
- **Framework:** FastAPI with Uvicorn
- **Port:** 8000 (forwarded in devcontainer)
- **Auto-reload:** Enabled via `watchfiles` dependency

### Required Dependencies
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `httpx` - HTTP client (for testing)
- `watchfiles` - Auto-reload functionality

## Exercise Context

This is a GitHub Skills exercise repository. The repo includes GitHub Workflows (`.github/workflows/`) that track progress through exercise steps. These workflows are part of the exercise framework and should not be modified for feature development.
