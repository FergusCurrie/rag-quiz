import logging
import random
from backend.connections import get_postgres_db
from backend.crud import create_review, get_all_questions, get_question
from backend.llm_interface.InterfaceJudgeResponse import InterfaceJudgeResponse
from backend.logging_config import LOGGING_CONFIG
from backend.models import PromptStore
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

JUDGE_PROMPT_TYPE = "judge_answer"

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"],  # Add this line
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/api/question")
async def get_next_question(db: Session = Depends(get_postgres_db)):
    questions = get_all_questions(db)
    if len(questions) == 0:
        raise Exception("Empty list of questions...")
    question = random.choice(questions)
    return {"question": question.question, "question_id": question.question_id}


class Submission(BaseModel):
    user_answer: str
    question_id: str
    # time_taken: int


@app.post("/api/answer")
async def post_answer(submission: Submission, db: Session = Depends(get_postgres_db)):
    question = get_question(db, submission.question_id)
    # Get most recent prompt for judge
    prompt_record = (
        db.query(PromptStore)
        .filter(PromptStore.prompt_type == JUDGE_PROMPT_TYPE)
        .order_by(PromptStore.created_date.desc())
        .first()
    )
    if not prompt_record:
        raise Exception("No judge prompt found in database")
    judge_interface = InterfaceJudgeResponse(prompt_id=prompt_record.prompt_id, prompt=prompt_record.prompt)
    llm_response = judge_interface.judge_quiz_answer(question.question, submission.user_answer, question.answer)
    return {
        "llm_response": llm_response["response"],
        "llm_score": llm_response["score"],
        "prompt_id": llm_response["prompt_id"],
    }


class ReviewData(BaseModel):
    user_answer: str
    question_id: str
    time_taken: int
    llm_response: str
    llm_score: int
    user_rating: int
    prompt_id: str


@app.post("/api/review")
async def post_review(review_data: ReviewData, db: Session = Depends(get_postgres_db)):
    question = get_question(db, review_data.question_id)
    db_review = create_review(
        db,
        concept_id=question.concept_id,
        question_id=question.question_id,
        time_taken=review_data.time_taken,
        llm_response=review_data.llm_response,
        llm_model="gpt-4o",
        llm_rating=review_data.llm_score,
        user_response=review_data.user_answer,
        user_rating=review_data.user_rating,
        prompt_id=review_data.prompt_id,
    )

    return {}

    # print(f'Question: {question.question}')
    # user_answer = input('> ')
    # response = judge_quiz_answer(question, user_answer, question.answer)
    # print(f"LLM response: {response['response']}")
    # print(f"LLM score: {response['score']}")

    # db_review = create_review(db, question.concept_id, question.question_id, response['response'], 'gpt-4o', response['score'], user_answer )
    # print(db_review)
