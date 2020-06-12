from waitress import serve
from backend.api import app 
  
if __name__ == "__main__": 
    serve(app)
