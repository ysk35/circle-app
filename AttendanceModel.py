from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from setting import Base
from setting import ENGINE


class Attendance(Base):
  __tablename__ = "attendance"
  id = Column('id', Integer, primary_key = True)
  user_id = Column('user_id', Integer)
  name = Column('name', String(200))
  date = Column('date', Date)

if __name__ == "__main__":
  Base.metadata.drop_all(ENGINE)
  Base.metadata.create_all(bind=ENGINE)