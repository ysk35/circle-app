from sqlalchemy import Boolean, Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = "sqlite:///./app.db"

engine = create_engine(
  SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, echo=True
)

Base = declarative_base()

# テーブルの定義
class User(Base):
  __tablename__ = 'users'
  id = Column('id', Integer, primary_key = True)
  line_user_id = Column('line_user_id', String(200))
  name = Column('name', String(200))
  student_number= Column('student_number', String(200))

# class Attendance(Base):
#   __tablename__ = "attendance"
#   id = Column('id', Integer, primary_key = True)
#   user_id = Column('usser_id', Integer)
#   name = Column('name', String(200))
#   date = Column('date', Date)

# テーブル作成
Base.metadata.create_all(bind=engine)