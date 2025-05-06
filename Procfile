web: gunicorn gardengals.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 60 --log-file -
# Temporarily change the release command for debugging - simpler print
release: python -c "import os; print('--- DEBUG: DATABASE_URL in release command is: ' + str(os.environ.get('DATABASE_URL')))" 