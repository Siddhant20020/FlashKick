from flask import Flask
from routes import main
from flask_cors import CORS
import os
import logging

# Configurinh logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Creating the upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Registering the blueprint
app.register_blueprint(main)

# Enabling CORS if frontend and backend are on different origins
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
