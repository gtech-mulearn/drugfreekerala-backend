from db.models import Base
from db.connection import engine

Base.metadata.create_all(bind=engine)
