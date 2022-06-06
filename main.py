from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
# from bson.objectid import ObjectId

import os
from dotenv import load_dotenv
import motor.motor_asyncio
from beanie import PydanticObjectId, Document, init_beanie
from pydantic import BaseModel

# from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase

load_dotenv()
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3333",
    "http://localhost",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

client = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb+srv://admin:{os.environ['MONGOPASSWORD']}@{os.environ['CLUSTER_URL']}/dep_db?retryWrites=true&w=majority",
    uuidRepresentation="standard")

db = client.dep_db
collection = db.test_collection


class FeatureProperties(BaseModel):
    description: str
    name: str
    current_name: Optional[str]


class Geometry(BaseModel):
    type: str = "Point"
    coordinates: List[float]


class Feature(BaseModel):
    type: str = "Feature"
    properties: FeatureProperties
    geometry: Geometry


class Case(Document):
    year: int
    nationality: str
    number: Optional[int]
    home: Feature
    exile: Feature
    sources: Optional[List[str]]

    class Settings:
        name = "test_collection"


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[Case]
    )


@app.get("/health")
async def health():
    return {"message": "OK"}


@app.get("/cases/filter")
async def filtered_locations(year: int):
    cases = await Case.find(Case.year == year).to_list()
    return cases


@app.get("/cases/{id}")
async def case_by_id(id):
    case = await Case.get(id)
    return case


@app.post("/cases", response_model=Case)
async def create_event(event: Case):
    new_event = await Case.insert_one(event)
    return new_event




# @app.put(`/events/{locationId}`)

# @app.post()
