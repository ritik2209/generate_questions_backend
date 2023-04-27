from fastapi import APIRouter, HTTPException
from app.utils.generate_questions_logic import generate_questions_from_model
from pydantic import BaseModel


router = APIRouter()

@router.post("/generate_questions", summary="Get questions from a Paragraph", description="Generates Questions from a Paragraph")
async def generate_questions(input_text:str):
    try:
        generated_questions = generate_questions_from_model(input_text)
        if len(generated_questions) == 0:
            raise HTTPException(status_code=404, detail="No questions could be generated from the input text.")
        return {"generated_questions": generated_questions}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while generating questions: {e}")

