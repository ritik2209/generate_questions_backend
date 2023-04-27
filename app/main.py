from fastapi import FastAPI
from app.routers import generate_questions_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Generate Questions API")
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_questions_router.router,tags=["Generate Questions"])