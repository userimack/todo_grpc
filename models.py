from sqlalchemy import create_engine, Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql://root@localhost/todo", echo=True, echo_pool=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(30), nullable=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    todos = relationship("Todo", backref="user")


class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(String(100), nullable=False)
    status = Column(Integer, nullable=False)

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text
