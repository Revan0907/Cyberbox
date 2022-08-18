from flask import Flask, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '6fff3d56b180be5fb38c37347cffcc0e66a0880f114c00ea' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql8513463:sPcSIaAsdk@sql8.freemysqlhosting.net:3306/sql8513463'

login_manager = LoginManager()
login_manager.init_app(app)

db= SQLAlchemy(app)

from website import routes
