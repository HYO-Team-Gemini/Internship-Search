import os

from waitress import serve

from backend.api import app

if __name__ == "__main__":
    try:
        port = os.getenv('PORT')
    except:
        port = 8080
    serve(app, port=port)
