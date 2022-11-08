from sqlalchemy import Column, Integer, String, ForeignKey, Date
from .db import Base, session
from enum import Enum


class TaskStatusEnum(str, Enum):
    TODO: str = "To do"
    DOING: str = "Doing"
    DONE: str = "Done"


def save_obj(obj: Base) -> None:
    session.add(obj)
    session.commit()
    session.refresh(obj)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(500), nullable=False)
    session_id = Column(String(100), nullable=True)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    admin = Column(Integer, ForeignKey("user.id"), nullable=False)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class ProjectMember(Base):
    __tablename__ = "project_member"
    id = Column(Integer, primary_key=True)
    project = Column(Integer, ForeignKey("project.id"), nullable=False)
    user = Column(Integer, ForeignKey("user.id"), nullable=False)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    project = Column(Integer, ForeignKey("project.id"), nullable=False)
    project_member = Column(Integer, ForeignKey("project_member.id"), nullable=False)
    text = Column(String(500), nullable=False)
    deadline = Column(Date, nullable=False)
    status = Column(String, nullable=False)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# the code below must be executed only one time before running flask app
# Base.metadata.create_all(engine)
