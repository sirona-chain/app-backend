# Sirona backend

This is the backend for our blockchain-enabled application.

### Setup

```bash
# Create a virtual environment
python -m venv .venv

# On MacOS, WSL, Linux
source .venv/bin/activate

# On Windows
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database
flask --app app.web init-db
```

### Running server

```bash
inv dev
```
