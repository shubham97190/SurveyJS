from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from .services import create_update_survey, get_survey, create_response, get_response, list_responses
from .model import SurveyCreate, SurveyOut, ResponseCreate, ResponseOut, doc_to_out
from .database import get_db

router = APIRouter(prefix="/v1/surveys", tags=["surveys"])

@router.post("", response_model=Dict[str, Any])
async def create_survey(payload: SurveyCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await create_update_survey(db, payload.model_dump())

@router.get("", response_model=Dict[str, Any])
async def list_surveys(db: AsyncIOMotorDatabase = Depends(get_db)):
    surveys = db["surveys"].find().limit(1).batch_size(100)
    doc = await surveys.next()
    return doc_to_out(doc)

@router.get("/{survey_id}", response_model=SurveyOut)
async def get_survey_by_id(survey_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    survey = await get_survey(db, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey

@router.post("/responses", response_model=Dict[str, Any])
async def create_survey_response(payload: ResponseCreate = Body(...), db: AsyncIOMotorDatabase = Depends(get_db)):
    if "survey_id" not in payload.model_dump():
        raise HTTPException(status_code=400, detail="survey_id required")
    return await create_response(db, payload.model_dump())

@router.get("/responses/{response_id}", response_model=ResponseOut)
async def get_survey_response(response_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    response = await get_response(db, response_id)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    return response

@router.get("/responses/by-survey/{survey_id}", response_model=Dict[str, List[ResponseOut]])
async def list_survey_responses(survey_id: str, limit: int = Query(20, ge=1, le=200), db: AsyncIOMotorDatabase = Depends(get_db)):
    response = await list_responses(db, survey_id, limit)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    return response