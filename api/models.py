import enum
from datetime import date
from typing import Set, Literal
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

type UserQualification = Literal["Matriculation",
                                 "Senior Secondary", "Graduation", "Post Graduation", "PhD"]
Base = declarative_base(type_annotation_map={
    UserQualification: Enum(enum.Enum),
})


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    qualification: Mapped[UserQualification] = mapped_column()
    dob: Mapped[date] = mapped_column()
    scores: Mapped[Set["Score"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")


class Subject(Base):
    __tablename__ = "subject"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(default="")
    chapters: Mapped[Set["Chapter"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan")
    quizzes: Mapped[Set["Quiz"]] = relationship(back_populates="subject")


class Chapter(Base):
    __tablename__ = "chapter"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(default="")
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    subject: Mapped["Subject"] = relationship(back_populates="chapters")
    quizzes: Mapped[Set["Quiz"]] = relationship(
        back_populates="chapter", cascade="all, delete-orphan")


class Quiz(Base):
    __tablename__ = "quiz"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"))
    date_of_quiz: Mapped[date]
    hours: Mapped[int] = mapped_column()
    minutes: Mapped[int] = mapped_column()
    remarks: Mapped[str] = mapped_column(default="")
    subject: Mapped["Subject"] = relationship(back_populates="quizzes")
    chapter: Mapped["Chapter"] = relationship(back_populates="quizzes")
    questions: Mapped[Set["Question"]] = relationship(
        back_populates="quiz", cascade="all, delete-orphan")
    scores: Mapped[Set["Score"]] = relationship(back_populates="quiz")


class Question(Base):
    __tablename__ = "question"
    id: Mapped[int] = mapped_column(primary_key=True)
    statement: Mapped[str]
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"))
    quiz: Mapped["Quiz"] = relationship("Quiz")
    correct: Mapped[int] = mapped_column(ForeignKey("question.id"))
    options: Mapped[Set["Option"]] = relationship(cascade="all, delete-orphan")


class Option(Base):
    __tablename__ = "option"
    id: Mapped[int] = mapped_column(primary_key=True)
    statement: Mapped[str]
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))


class Score(Base):
    __tablename__ = "score"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"))
    user_score: Mapped[int]
    total_score: Mapped[int]
    user: Mapped["User"] = relationship("User")
    quiz: Mapped["Quiz"] = relationship("Quiz")
