# app/models.py

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from app.database import Base

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True)

    repo_name = Column(String, nullable=False, unique=True)

    owner = Column(String)

    language = Column(String)

    stars = Column(Integer)

    forks = Column(Integer)

    open_issues = Column(Integer)

    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    scraped_at = Column(DateTime)