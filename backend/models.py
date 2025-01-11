from datetime import datetime
import uuid
from typing import List
from sqlalchemy import ForeignKey, String, Integer, Boolean, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class PromptStore(Base):
    __tablename__ = "prompt_store"

    prompt_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_date: Mapped[datetime] = mapped_column(default=func.now())

class ConceptStore(Base):
    __tablename__ = "concept_store"

    concept_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_date: Mapped[datetime] = mapped_column(default=func.now())
    user_created: Mapped[bool] = mapped_column(Boolean, default=False)

    reviews: Mapped[List["Review"]] = relationship(back_populates="concept")
    from_relationships: Mapped[List["KnowledgeGraph"]] = relationship(foreign_keys="[KnowledgeGraph.from_concept_id]")
    to_relationships: Mapped[List["KnowledgeGraph"]] = relationship(foreign_keys="[KnowledgeGraph.to_concept_id]")

class Question(Base):
    __tablename__ = "questions"

    question_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question: Mapped[str]
    answer: Mapped[str]
    created_date: Mapped[datetime] = mapped_column(default=func.now())

    reviews: Mapped[List["Review"]] = relationship(back_populates="question")

class Review(Base):
    __tablename__ = "reviews"

    review_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_date: Mapped[datetime] = mapped_column(default=func.now())
    llm_response: Mapped[str | None]
    llm_model: Mapped[str | None]
    llm_rating: Mapped[int | None]
    concept_id: Mapped[UUID] = mapped_column(ForeignKey("concept_store.concept_id"))
    question_id: Mapped[UUID] = mapped_column(ForeignKey("questions.question_id"))
    user_response: Mapped[str | None]

    concept: Mapped["ConceptStore"] = relationship(back_populates="reviews")
    question: Mapped["Question"] = relationship(back_populates="reviews")

class KnowledgeGraph(Base):
    __tablename__ = "kg_db"

    kg_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_date: Mapped[datetime] = mapped_column(default=func.now())
    from_concept_id: Mapped[UUID] = mapped_column(ForeignKey("concept_store.concept_id"))
    to_concept_id: Mapped[UUID] = mapped_column(ForeignKey("concept_store.concept_id"))
    relationship: Mapped[str]

    from_concept: Mapped["ConceptStore"] = relationship(foreign_keys=[from_concept_id])
    to_concept: Mapped["ConceptStore"] = relationship(foreign_keys=[to_concept_id])

    