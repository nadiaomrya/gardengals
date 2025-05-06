web: gunicorn gardengals.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 60 --log-file -
# Temporarily change the release command for debugging
release: python -c "import os; print(f'--- DEBUG: DATABASE_URL in release command: {os.environ.get("DATABASE_URL")}')" 