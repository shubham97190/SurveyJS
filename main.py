from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import router as survey_router
from app.database import client, db
from fastapi.middleware.cors import CORSMiddleware
# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure MongoDB connection
    await db.command("ping")
    yield
    # Shutdown: Close MongoDB client
    client.close()

origins = [
    "*",
]

# Initialize FastAPI app with lifespan
app = FastAPI(title="SurveyJS API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include survey router
app.include_router(survey_router)