from api.models import *
from datetime import datetime
from api.database import session
from flask_restful import Resource, Api
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, update
from flask import request, jsonify, make_response
from flask_jwt_extended import JWTManager, jwt_required, current_user


api = Api()
jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email


@jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data):
    identity = jwt_data["sub"]
    return session.execute(select(User).where(User.email == identity)).scalar()


class Subjects(Resource):
    @jwt_required()
    def get(self):
        return jsonify(subjects=[
            {
                "id": subject.id,
                "name": subject.name,
                "description": subject.description,
                "chapters": [
                    {"id": chapter.id, "name": chapter.name,
                     "description": chapter.description}
                    for chapter in subject.chapters
                ],
            }
            for subject in session.execute(select(Subject)).scalars()
        ])

    @jwt_required()
    def post(self):
        try:
            subject = request.get_json()
            chapters = subject.pop("chapters")

            subject = Subject(
                name=subject["name"], description=subject["description"])
            session.add(subject)
            session.commit()

            chapters = {
                Chapter(
                    name=chapter["name"],
                    description=chapter["description"],
                    subject_id=subject.id,
                )
                for chapter in chapters
            }
            session.add_all(chapters)
            session.commit()
            return make_response('subject created successfully', 201)
        except IntegrityError:
            return make_response('subject already exists', 400)

    @jwt_required()
    def delete(self, subject_id: int):
        try:
            session.execute(delete(Subject).where(Subject.id == subject_id))
            session.commit()
            return make_response('subject deleted successfully')
        except IntegrityError:
            return make_response('failed to delete subject', 500)
        except Exception as error:
            return make_response(f'unknown error {error}', 500)


class Quizzes(Resource):
    @jwt_required()
    def get(self, quiz_id: int | None = None):
        if quiz_id is not None:
            quizzes = session.execute(
                select(Quiz).where(Quiz.id == quiz_id).join(
                    Score, Score.user_id != current_user.id)
            ).scalar()
            return jsonify(quizzes)
        return jsonify(quizzes=[
            {
                "quiz_id": quiz.id,
                "name": quiz.name,
                "remarks": quiz.remarks,
                "subject": quiz.chapter.subject.name,
                "chapter": quiz.chapter.name,
                "hh": quiz.hours,
                "mm": quiz.minutes,
                "date_of_quiz": quiz.date_of_quiz,
                "questions": [
                    {
                        "id": question.id,
                        "statement": question.statement,
                        "options": [
                            {
                                "id": option.id,
                                "statement": option.statement
                            } for option in question.options
                        ],
                    }
                    for question in quiz.questions
                ],
                "done": current_user in (score.user for score in quiz.scores)
            }
            for quiz in session.execute(select(Quiz)).scalars()
        ])

    @jwt_required()
    def post(self):
        try:
            print(current_user.email)
            quiz = request.json

            questions = quiz.pop("questions")
            quiz = Quiz(
                name=quiz["name"],
                remarks=quiz["remarks"],
                subject_id=int(quiz["subject"]),
                chapter_id=int(quiz["chapter"]),
                date_of_quiz=datetime.strptime(
                    quiz["date_of_quiz"], "%Y-%m-%d"
                ).date(),
                hours=int(quiz["hh"]),
                minutes=int(quiz["mm"]),
            )

            session.add(quiz)
            session.commit()
            for question in questions:
                options = question.pop("options")
                answer = question.pop("answer")
                print(answer)
                question = Question(
                    statement=question.pop("statement"), quiz_id=quiz.id,
                    correct=answer
                )
                session.add(question)
                session.commit()
                options = [
                    Option(
                        statement=option['statement'],
                        question_id=question.id,
                    )
                    for option in options
                ]
                session.add_all(options)
                session.commit()
                session.execute(update(Question).where(
                    Question.id == question.id).values(correct=options[answer].id))
                session.commit()
            return make_response('quiz created successfully', 201)
        except IntegrityError:
            return make_response('failed to create quiz', 500)
        except Exception as error:
            return make_response(f'unknown error {error}', 500)

    @jwt_required()
    def delete(self, quiz_id: int):
        try:
            quiz = session.execute(select(Quiz).where(
                Quiz.id == quiz_id)).scalar()
            session.delete(quiz)
            session.commit()
            return make_response('quiz deleted successfully', 200)
        except IntegrityError as error:
            print(error)
            return make_response('failed to delete quiz!', 500)
        except Exception as error:
            return make_response(f'unknown error: {error}', 500)


class UserScores(Resource):
    @jwt_required()
    def get(self):
        try:
            print([score.user_score for score in current_user.scores])
            return jsonify({
                "scores": [
                    {
                        "total": score.total_score,
                        "correct": score.user_score,
                        "date_of_quiz": score.quiz.date_of_quiz,
                        "id": score.id,
                        "subject_id": score.quiz.subject_id,
                    }
                    for score in current_user.scores
                ]
            })
        except IntegrityError:
            return make_response('failed to fetch user scores', 500)
        except Exception as error:
            return make_response(f'unknown error: {error}', 500)


api.add_resource(Quizzes, "/api/quizzes", "/api/quizzes/<int:quiz_id>")
api.add_resource(Subjects, "/api/subjects", "/api/subjects/<int:subject_id>")
api.add_resource(UserScores, "/api/scores")
