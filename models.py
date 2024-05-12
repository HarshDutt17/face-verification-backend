from sqlalchemy import Column, Integer, String, ARRAY
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    faces = Column(ARRAY(String))