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


from sqlalchemy import Boolean


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id = Column(Integer, primary_key=True, index=True)

    pipeline_name = Column(String, nullable=False)

    start_time = Column(DateTime, nullable=False)

    end_time = Column(DateTime)

    duration_seconds = Column(Integer)

    status = Column(String, nullable=False)

    rows_extracted = Column(Integer, default=0)

    rows_loaded = Column(Integer, default=0)

    error_message = Column(String, nullable=True)