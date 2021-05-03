from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '6fff3d56b180be5fb38c37347cffcc0e66a0880f114c00ea' #Check again if error persists
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c2053192:BF4V2ZiBun3U2Ta@csmysql.cs.cf.ac.uk:3306/c2053192_database1'

login_manager = LoginManager()
login_manager.init_app(app)

db= SQLAlchemy(app)

from website import routes
