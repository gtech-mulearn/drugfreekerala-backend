from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserData(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    # NULL means the pledge was made before the form asked.
    is_student = Column(Boolean, nullable=True)
    # µLearn college UUID; NULL when the student typed a name under "Other".
    college_id = Column(String(36), nullable=True)
    college_name = Column(String(255), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
