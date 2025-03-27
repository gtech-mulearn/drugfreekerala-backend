from fastapi import Depends, FastAPI, Query
from fastapi.responses import ORJSONResponse
from pydantic import EmailStr
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from starlette import status
from db.connection import get_session
from db.models import UserData
from schemas import CreateUserDataRequest
from settings import settings
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

application = FastAPI(default_response_class=ORJSONResponse)


application.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@application.head("/ping")
async def ping():
    return HTMLResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)


@application.post("/drugfreekerala/create", description="Create a new user")
async def create(data: CreateUserDataRequest, session: Session = Depends(get_session)):
    try:
        data = UserData(name=data.name, email=data.email)
        session.add(data)
        session.commit()
        return {"message": "User created"}
    except IntegrityError:
        return {"message": "User already exists"}


@application.get("/drugfreekerala/get", description="Get all users")
async def get_all_users(
    session: Session = Depends(get_session), email: EmailStr = Query(...)
):
    data = session.query(UserData).filter(UserData.email == email).first()
    return {
        "id": data.id,
        "name": data.name,
        "email": data.email,
    }


@application.get("/drugfreekerala/total", description="Get total number of users")
async def get_total_users(session: Session = Depends(get_session)):
    data = session.query(UserData).count()
    return {"total": data}
