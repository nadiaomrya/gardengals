web: gunicorn gardengals.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 60 --log-file -
# Simplest possible release command for debugging
release: echo "--- DEBUG: Procfile release command is running. DATABASE_URL is $DATABASE_URL" 