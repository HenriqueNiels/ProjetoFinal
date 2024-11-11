from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '@sukitoslacancei'

db = SQLAlchemy(app)
login_manager = LoginManager()
migrate = Migrate(app,db)
login_manager.init_app(app)
bcrypt = Bcrypt(app)

from app.routes import homepage
from app.models import User