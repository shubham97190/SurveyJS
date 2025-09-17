from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import timezone
from typing import Dict, Any, Optional, List
from datetime import datetime
from .model import oid, doc_to_out, ResponseOut


async def create_survey(db: AsyncIOMotorDatabase, payload: Dict[str, Any]) -> Dict[str, Any]:
    col = db["surveys"]
    now = datetime.now(timezone.utc)
    doc = {"data": payload, "created_at": now, "updated_at": now}
    res = await col.insert_one(doc)
    return {"id": str(res.inserted_id), "created_at": now}

async def create_update_survey(db: AsyncIOMotorDatabase, payload: Dict[str, Any]) -> Dict[str, Any]:
    col = db["surveys"]
    now = datetime.now(timezone.utc)
    
    # Check if any survey document exists
    existing_survey = await col.find_one({})
    
    if existing_survey:
        # Update the existing survey
        update_doc = {
            "$set": {
                "data": payload.get("data", {}),
                "updated_at": now
            }
        }
        await col.update_one({"_id": existing_survey["_id"]}, update_doc)
        updated_survey = await col.find_one({"_id": existing_survey["_id"]})
        return doc_to_out(updated_survey)
    
    # Create a new survey if none exists
    doc = {
        "data": payload.get("data", {}),
        "created_at": now,
        "updated_at": now
    }
    res = await col.insert_one(doc)
    new_survey = await col.find_one({"_id": res.inserted_id})
    return doc_to_out(new_survey)


async def get_survey(db: AsyncIOMotorDatabase, survey_id: str) -> Optional[Dict[str, Any]]:
    col = db["surveys"]
    doc = await col.find_one({"_id": oid(survey_id)})
    return doc_to_out(doc) if doc else None


async def create_response(db: AsyncIOMotorDatabase, payload: Dict[str, Any]) -> Dict[str, Any]:
    col = db["responses"]
    now = datetime.now(timezone.utc)
    doc = {
        "survey_id": payload["survey_id"],
        "data": payload.get("data", {}),
        "created_at": now,
        "updated_at": now,
    }
    res = await col.insert_one(doc)
    return {"id": str(res.inserted_id), "created_at": now}


async def get_response(db: AsyncIOMotorDatabase, response_id: str) -> Optional[Dict[str, Any]]:
    col = db["responses"]
    doc = await col.find_one({"_id": oid(response_id)})
    return doc_to_out(doc) if doc else None


async def list_responses(db: AsyncIOMotorDatabase, survey_id: Optional[str] = None, limit: int = 20) -> Dict[str, List[Dict[str, Any]]]:
    col = db["responses"]
    query = {"survey_id": oid(survey_id)} if survey_id else {}
    items: List[Dict[str, Any]] = []
    cursor = col.find(query).sort("_id", -1).limit(limit).batch_size(100)
    items = [doc_to_out(doc) async for doc in cursor]
    # items = [ResponseOut(**doc_to_out(doc)).model_dump() async for doc in cursor]
    return {"items": items}