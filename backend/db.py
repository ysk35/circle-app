from flask import Flask
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  line_user_id = db.Column(db.String(200))
  name = db.Column(db.String(200))
  student_number = db.Column(db.String(200))

class Attendance(db.Model):
  __tablename__ = "attendance"
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer)
  name = db.Column(db.String(200))
  date = db.Column(db.Date)

class AdminUser(UserMixin, db.Model):
  __tablename__ = "admin_users"
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(200))
  password = db.Column(db.String(200))

# テーブル作成
if __name__ == '__main__':
  db.create_all()
  # db.app_context().push()