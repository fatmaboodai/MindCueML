workers = 20  # Adjust the number of worker processes based on your server's CPU cores
bind = "0.0.0.0:8080"  # Specify the host and port for Gunicorn
app_module = "app:app"  # Replace "your_app" with the name of your Flask application instance
# waitress-serve --port=8080 app:app