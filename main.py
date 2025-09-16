from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import router as survey_router
from app.database import client, db

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure MongoDB connection
    await db.command("ping")
    yield
    # Shutdown: Close MongoDB client
    client.close()

# Initialize FastAPI app with lifespan
app = FastAPI(title="SurveyJS API", lifespan=lifespan)

# Include survey router
app.include_router(survey_router)