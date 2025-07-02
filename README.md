# Feature Flag Management Service

A simple service for managing feature flags.

## Setup

1.  Create a virtual environment: `python -m venv venv`
2.  Activate the virtual environment: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
3.  Install dependencies: `pip install -r backend/requirements.txt`
4.  Set up the database:
    ```bash
    export FLASK_APP=backend/app.py  # or set DATABASE_URL environment variable directly
    flask db init
    flask db migrate
    flask db upgrade
    ```
5.  Run the backend: `python backend/app.py`
6.  Open `frontend/index.html` in your browser.

## API Endpoints

*   `GET /features`: Get all feature flags.
*   `GET /features/<name>`: Get a specific feature flag by name.
*   `POST /features`: Create a new feature flag.
*   `PUT /features/<name>`: Update an existing feature flag.
*   `DELETE /features/<name>`: Delete a feature flag.

## Running Tests

```bash
python backend/tests/test_app.py
```