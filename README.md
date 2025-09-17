# SurveyJS - FastAPI Survey Management System

A robust FastAPI-based survey management system that allows you to create, update, and manage surveys along with their responses. Built with FastAPI, MongoDB, and modern Python async features.

## Features

- Create and update surveys
- Single survey instance management
- Collect survey responses
- Retrieve individual responses
- List all responses for a survey
- Built with async/await for better performance
- MongoDB for flexible data storage
- Pydantic models for data validation

## Tech Stack

- Python 3.x
- FastAPI
- MongoDB
- Motor (async MongoDB driver)
- Pydantic
- Uvicorn

## Project Structure

```
SurveyJS/
├── app/
│   ├── __init__.py
│   ├── database.py     # Database connection and configuration
│   ├── model.py        # Pydantic models for data validation
│   ├── routers.py      # API route definitions
│   └── services.py     # Business logic and database operations
├── main.py            # Application entry point
└── requirements.txt   # Project dependencies
```

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/shubham97190/SurveyJS.git
cd SurveyJS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure you have MongoDB running locally or update the connection string in `database.py`

4. Run the application:
```bash
uvicorn main:app --reload --port 8009 --host 0.0.0.0
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Surveys

- **List Surveys**
  - GET `/v1/surveys`
  - Query Parameters:
    - `limit`: Maximum number of surveys to return (default: 20, max: 200)
  - Returns list of all surveys, newest first

- **Create/Update Survey**
  - POST `/v1/surveys`
  - Body: `{ "data": { ... } }`
  - Creates a new survey or updates the existing one

- **Get Survey**
  - GET `/v1/surveys/{survey_id}`
  - Retrieves a specific survey by ID

- **Delete All Surveys**
  - DELETE `/v1/surveys/all`
  - Deletes all surveys and their associated responses
  - Returns count of deleted surveys and responses

### Responses

- **Create Response**
  - POST `/v1/surveys/responses`
  - Body: `{ "survey_id": "...", "data": { ... } }`
  - Creates a new response for a survey

- **Get Response**
  - GET `/v1/surveys/responses/{response_id}`
  - Retrieves a specific response by ID

- **List Survey Responses**
  - GET `/v1/surveys/responses/by-survey/{survey_id}`
  - Query Parameters:
    - `limit`: Maximum number of responses to return (default: 20, max: 200)
  - Lists all responses for a specific survey

## Data Models

### Survey
```python
{
    "data": dict,            # Survey structure and content
    "id": str,              # Survey ID
    "created_at": datetime, # Creation timestamp
    "updated_at": datetime  # Last update timestamp
}
```

### Response
```python
{
    "survey_id": str,       # ID of the survey this response belongs to
    "data": dict,          # Response data
    "id": str,             # Response ID
    "created_at": datetime, # Creation timestamp
    "updated_at": datetime  # Last update timestamp
}
```

## Error Handling

The API includes proper error handling for common scenarios:
- 404 Not Found: When requested survey or response doesn't exist
- 400 Bad Request: When required fields are missing
- Validation errors: When the request data doesn't match the expected format

## Development

The project uses FastAPI's automatic API documentation. Once the server is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`
