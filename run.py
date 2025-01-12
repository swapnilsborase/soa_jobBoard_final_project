#run.py

from flask import Flask
from flasgger import Swagger
from app import create_app, mongo

app = create_app()

# Initialize Swagger
swagger = Swagger(app)

if __name__ == "__main__":
     app.run(host="0.0.0.0", port=8000)
