from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config')
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

from .routes import routes
from .views import index, authentication