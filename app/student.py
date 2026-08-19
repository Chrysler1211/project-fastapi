from fastapi import FastAPI
from . import models
from .database import Engine, get_db
from .router import Account, Profile,votes
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind = Engine)

app = FastAPI()


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def message():

    return {"Message": "Hello world"}





app.include_router(Account.router)
app.include_router(Profile.router)
app.include_router(votes.router)


