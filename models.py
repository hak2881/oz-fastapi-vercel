from datetime import datetime

from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey, Enum
from sqlalchemy.orm import relationship

from database import Base, engine
from enum import Enum as Task_enum

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, nullable=False,unique=True)
    email = Column(String)
    password = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="user", cascade="all, delete")

class TaskStatus(str, Task_enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    created_at = Column(DATETIME, default=datetime.utcnow)

    user_id = Column(ForeignKey("users.user_id"), nullable=False)
    user = relationship("User", back_populates="tasks")


Base.metadata.create_all(engine)