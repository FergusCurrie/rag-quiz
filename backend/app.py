
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.connections import get_postgres_db, get_postgres_conn
from sqlalchemy import text
from backend.models import Base
from sqlalchemy import create_engine
from backend.crud import create_concept, create_question, get_all_questions, create_review, get_all_reviews, get_question
from backend.qa import query_concept_quiz, judge_quiz_answer
import random
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging 
from backend.logging_config import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


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
        raise Exception('Empty list of questions...')
    question = random.choice(questions)
    return {'question' : question.question, 'question_id' : question.question_id}



class Submission(BaseModel):
    user_answer: str
    question_id: str

@app.post("/api/answer")
async def submit_question_answer(submission: Submission, db: Session = Depends(get_postgres_db)):
    question = get_question(db, submission.question_id)
    llm_response = judge_quiz_answer(question.question, submission.user_answer, question.answer)
    db_review = create_review(db, question.concept_id, question.question_id, llm_response['response'], 'gpt-4o', llm_response['score'], submission.user_answer)
    return {'llm_response' : llm_response['response'], 'llm_score': llm_response['score']}

    # print(f'Question: {question.question}')
    # user_answer = input('> ')
    # response = judge_quiz_answer(question, user_answer, question.answer)
    # print(f"LLM response: {response['response']}")
    # print(f"LLM score: {response['score']}")

    # db_review = create_review(db, question.concept_id, question.question_id, response['response'], 'gpt-4o', response['score'], user_answer )
    # print(db_review)
