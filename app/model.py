from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from bson import ObjectId


def oid(str_id: str) -> ObjectId:
    """Convert string ID to MongoDB ObjectId."""
    try:
        return ObjectId(str_id)
    except Exception as e:
        return str_id


def doc_to_out(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB document to JSON-compatible output."""
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    if "survey_id" in doc and isinstance(doc["survey_id"], ObjectId):
        doc["survey_id"] = str(doc["survey_id"])
    return doc


class SurveyBase(BaseModel):
    data: List[Dict[str, Any]]


class SurveyCreate(SurveyBase):
    pass


class SurveyOut(SurveyBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class ResponseBase(BaseModel):
    survey_id: str
    data: Dict[str, Any]


class ResponseCreate(ResponseBase):
    pass


class ResponseOut(ResponseBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}
