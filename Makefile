.PHONY: dev init-db test clean

# Starts the FastAPI server with live-reloading
dev:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Runs the database creation script
init-db:
	python scripts/seed_database.py

# Cleans up python cache files to prevent weird import bugs
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Installs all required dependencies
install:
	pip install -r requirements.txt
