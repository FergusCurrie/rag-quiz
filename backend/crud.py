from backend import models
from sqlalchemy.orm import Session
from uuid import UUID


def create_concept(db: Session, concept: str, user_created: bool = False) -> models.ConceptStore:
    """Create a new concept in the database"""
    db_concept = models.ConceptStore(
        concept=concept,
        user_created=user_created
    )
    db.add(db_concept)
    db.commit()
    db.refresh(db_concept)
    return db_concept

def get_concept(db: Session, concept_id: UUID) -> models.ConceptStore | None:
    """Retrieve a concept by its ID"""
    return db.query(models.ConceptStore).filter(
        models.ConceptStore.concept_id == concept_id
    ).first()


def get_concept_by_name(db: Session, concept: str) -> models.ConceptStore | None:
    """Retrieve a concept by its name"""
    return db.query(models.ConceptStore).filter(
        models.ConceptStore.concept == concept
    ).first()


def update_concept(
    db: Session, 
    concept_id: UUID, 
    concept: str | None = None,
    user_created: bool | None = None
) -> models.ConceptStore | None:
    """Update a concept's attributes"""
    db_concept = get_concept(db, concept_id)
    if db_concept is None:
        return None
    
    if concept is not None:
        db_concept.concept = concept
    if user_created is not None:
        db_concept.user_created = user_created
    
    db.commit()
    db.refresh(db_concept)
    return db_concept

def delete_concept(db: Session, concept_id: UUID) -> bool:
    """Delete a concept from the database"""
    db_concept = get_concept(db, concept_id)
    if db_concept is None:
        return False
    
    db.delete(db_concept)
    db.commit()
    return True

def create_prompt(db: Session) -> models.PromptStore:
    """Create a new prompt in the database"""
    db_prompt = models.PromptStore()
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def get_prompt(db: Session, prompt_id: UUID) -> models.PromptStore | None:
    """Retrieve a prompt by its ID"""
    return db.query(models.PromptStore).filter(
        models.PromptStore.prompt_id == prompt_id
    ).first()

def update_prompt(
    db: Session, 
    prompt_id: UUID,
    # Add more parameters here when you add more fields to the model
) -> models.PromptStore | None:
    """Update a prompt's attributes"""
    db_prompt = get_prompt(db, prompt_id)
    if db_prompt is None:
        return None
    
    # Add update logic here when you add more fields to the model
    
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def delete_prompt(db: Session, prompt_id: UUID) -> bool:
    """Delete a prompt from the database"""
    db_prompt = get_prompt(db, prompt_id)
    if db_prompt is None:
        return False
    
    db.delete(db_prompt)
    db.commit()
    return True

def create_question(
    db: Session, 
    question: str,
    answer: str,
    concept_id: UUID
) -> models.Question:
    """Create a new question in the database"""
    db_question = models.Question(
        question=question,
        answer=answer,
        concept_id=concept_id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_question(db: Session, question_id: UUID) -> models.Question | None:
    """Retrieve a question by its ID"""
    return db.query(models.Question).filter(
        models.Question.question_id == question_id
    ).first()

def get_all_questions(db: Session) -> list[models.Question]:
    """Retrieve all questions from the database"""
    return db.query(models.Question).all()


def update_question(
    db: Session, 
    question_id: UUID,
    question: str | None = None,
    answer: str | None = None,
    concept_id: UUID | None = None
) -> models.Question | None:
    """Update a question's attributes"""
    db_question = get_question(db, question_id)
    if db_question is None:
        return None
    
    if question is not None:
        db_question.question = question
    if answer is not None:
        db_question.answer = answer
    if concept_id is not None:
        db_question.concept_id = concept_id
    
    db.commit()
    db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: UUID) -> bool:
    """Delete a question from the database"""
    db_question = get_question(db, question_id)
    if db_question is None:
        return False
    
    db.delete(db_question)
    db.commit()
    return True

def create_review(
    db: Session,
    concept_id: UUID,
    question_id: UUID,
    llm_response: str | None = None,
    llm_model: str | None = None,
    llm_rating: int | None = None,
    user_response: str | None = None
) -> models.Review:
    """Create a new review in the database"""
    db_review = models.Review(
        concept_id=concept_id,
        question_id=question_id,
        llm_response=llm_response,
        llm_model=llm_model,
        llm_rating=llm_rating,
        user_response=user_response
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_review(db: Session, review_id: UUID) -> models.Review | None:
    """Retrieve a review by its ID"""
    return db.query(models.Review).filter(
        models.Review.review_id == review_id
    ).first()

def get_all_reviews(db: Session) -> list[models.Review]:
    """Retrieve all reviews from the database"""
    return db.query(models.Review).all()


def update_review(
    db: Session,
    review_id: UUID,
    llm_response: str | None = None,
    llm_model: str | None = None,
    llm_rating: int | None = None,
    user_response: str | None = None
) -> models.Review | None:
    """Update a review's attributes"""
    db_review = get_review(db, review_id)
    if db_review is None:
        return None
    
    if llm_response is not None:
        db_review.llm_response = llm_response
    if llm_model is not None:
        db_review.llm_model = llm_model
    if llm_rating is not None:
        db_review.llm_rating = llm_rating
    if user_response is not None:
        db_review.user_response = user_response
    
    db.commit()
    db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: UUID) -> bool:
    """Delete a review from the database"""
    db_review = get_review(db, review_id)
    if db_review is None:
        return False
    
    db.delete(db_review)
    db.commit()
    return True