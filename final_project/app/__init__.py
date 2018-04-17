from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flask_bootstrap import Bootstrap

app = Flask(__name__) # instance of class Flask
app.config.from_object(Config)
db = SQLAlchemy(app) # database
migrate = Migrate(app, db) # set-up migration
#bootstrap = Bootstrap(app) # to pretty-fy things

from app import routes, models
