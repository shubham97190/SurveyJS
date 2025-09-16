from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB client setup
client = AsyncIOMotorClient("mongodb+srv://shubham_db:Shubham9633#$@shubham.rcw5p.mongodb.net")
db = client["survey_db"]

async def get_db():
    return db