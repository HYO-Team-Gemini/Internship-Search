import os

from uszipcode import SearchEngine
from waitress import serve

from backend.api import app

search = SearchEngine(db_file_dir="backend/tmp")

if __name__ == "__main__":
    try:
        port = os.getenv('PORT')
        serve(app, port=port)
    except:
        port = 8080
        serve(app, port=port)
