from models import *
from database import session
from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource, Api
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, update
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager, jwt_required, current_user
from matplotlib import pyplot as plt


api = Api()
jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email

@jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data):
    identity = jwt_data["sub"]
    return session.execute(select(User).where(User.email == identity)).scalar()

class Users(Resource):
    @jwt_required()
    def get(self):
        return jsonify(current_user=dict(
            id=current_user.id,
            name=current_user.name,
            isAdmin=current_user.email=='admin@qm.xyz'
        ))

    def post(self):
        try:
            user = request.json
            user = User(
                name=user.get("name"),
                email=user.get("email"),
                password=generate_password_hash(user.get("password")),
                qualification=user.get("qualification"),
                dob=datetime.strptime(user.get("dob"), "%Y-%m-%d").date(),
            )
            session.add(user)
            session.commit()

            return jsonify(message='user created successfully', code=201)
        except IntegrityError:
            return jsonify(message='user already exists', code=400)


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
            return jsonify(message='subject created successfully', code=201)
        except IntegrityError:
            return jsonify(message='subject already exists', code=400)

    @jwt_required()
    def delete(self, subject_id: int):
        try:
            session.execute(delete(Subject).where(Subject.id == subject_id))
            session.commit()
            return jsonify(message='subject deleted successfully')
        except IntegrityError:
            return jsonify(message='failed to delete subject', code=500)
        except Exception as error:
            return jsonify(message=f'unknown error {error}', code=500)


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
            return jsonify(message='quiz created successfully', code=201)
        except IntegrityError:
            return jsonify(message='failed to create quiz', code=500)
        except Exception as error:
            return jsonify(message=f'unknown error {error}', code=500)

    @jwt_required()
    def delete(self, quiz_id: int):
        try:
            quiz = session.execute(select(Quiz).where(
                Quiz.id == quiz_id)).scalar()
            session.delete(quiz)
            session.commit()
            return jsonify(message='quiz deleted successfully')
        except IntegrityError as error:
            print(error)
            return jsonify(message='failed to delete quiz!', code=500)
        except Exception as error:
            return jsonify(message=f'unknown error: {error}', code=500)


class QuizSubmit(Resource):
    @jwt_required()
    def post(self):
        try:
            quiz_data = request.get_json()
            quiz = session.execute(select(Quiz).where(
                Quiz.id == quiz_data["quiz_id"])).scalar()

            user_score = 0
            for question in quiz.questions:
                if question.correct == quiz_data["selected"][str(question.id)]:
                    user_score += 1
            user_score = Score(user_id=current_user.id, quiz_id=quiz.id,
                               user_score=user_score, total_score=len(quiz.questions))
            session.add(user_score)
            session.commit()

            return jsonify(message='user score updated!', code=201)
        except IntegrityError:
            return jsonify(message='failed to delete quiz', code=409)
        except Exception as error:
            return jsonify(message=f'unknown error: {error}', code=500)


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
            return jsonify(message='failed to fetch user scores', code=500)
        except Exception as error:
            return jsonify(message=f'unknown error: {error}', code=500)


class Statistics(Resource):
    @jwt_required()
    def get(self):
        MONTHS = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        try:
            if current_user.email != 'admin@qm.xyz': # userwise quiz summary
                by_subject = {}
                by_month = {}
                for score in current_user.scores:
                    if score.quiz.subject.name not in by_subject:
                        by_subject[score.quiz.subject.name] = {
                            "name": score.quiz.subject.name,
                            "scores": [],
                            "average": 0,
                            "total": 0,
                            "score": 0,
                        }
                    if score.quiz.date_of_quiz.month not in by_month:
                        by_month[score.quiz.date_of_quiz.month] = {"month": score.quiz.date_of_quiz.month, "count": 0}
                    by_month[score.quiz.date_of_quiz.month]["count"] += 1

                    by_subject[score.quiz.subject.name]["scores"].append({
                        "total": score.total_score,
                        "correct": score.user_score,
                        "date_of_quiz": score.quiz.date_of_quiz,
                        "id": score.id,
                    })
                    by_subject[score.quiz.subject.name]["total"] += score.total_score
                    by_subject[score.quiz.subject.name]["score"] += score.user_score

                for subject in by_subject.values():
                    subject["average"] = subject["score"] / subject["total"]
                
                fig = plt.figure()
                plt.bar(by_subject.keys(), [subject["average"] for subject in by_subject.values()])
                plt.xlabel("Subjects")
                plt.ylabel("Average")
                filename_by_subject = f"by_subject-{hash(current_user.email)}.png"
                fig.savefig(f"public/images/{filename_by_subject}")

                fig = plt.figure()
                plt.pie(
                    by_month.keys(),
                    [month["count"] for month in by_month.values()], 
                    autopct="%1.1f%%", 
                    textprops=dict(color="w"))
                plt.legend(
                    [MONTHS[month-1] for month in by_month.keys()],
                    title="Months")
                filename_by_month = f"by_month-{hash(current_user.email)}.png"
                fig.savefig(f"public/images/{filename_by_month}")

                return jsonify(by_month=filename_by_month, by_subject=filename_by_subject, code=200)
            else: # admin subject wise summary
                by_subject = {}
                
                for score in session.execute(select(Score)).scalars():
                    if score.quiz.subject.name not in by_subject:
                        by_subject[score.quiz.subject.name] = {
                            "max_score": 0,
                            "user_count": 0
                        }
                    by_subject[score.quiz.subject.name]["max_score"] = max(
                        by_subject[score.quiz.subject.name]["max_score"], score.user_score / score.total_score)
                    by_subject[score.quiz.subject.name]["user_count"] += 1
                
                print(by_subject)
                fig = plt.figure()
                plt.bar(by_subject.keys(), [subject["max_score"] for subject in by_subject.values()])
                plt.xlabel("Subjects")
                plt.ylabel("Max Score")
                fig.savefig("public/images/admin_subject_wise.png")

                fig = plt.figure()
                plt.pie(
                    [subject["user_count"] for subject in by_subject.values()], 
                    labels=by_subject.keys(),
                    textprops=dict(color="w"),
                    autopct="%1.1f%%")
                plt.subplots_adjust(right=0.75)
                plt.legend(by_subject.keys(), title="Subjects", bbox_to_anchor=(0.90, 0.25, 0.5, 0.5))
                fig.savefig("public/images/admin_user_count.png")
                print('files written')

                return jsonify(user_count="admin_user_count.png", by_subject="admin_subject_wise.png", code=200)
        except IntegrityError:
            return jsonify(message='failed to ', code=500)
        except Exception as error:
            return jsonify(message=f'unknown error: {error}', code=500)


api.add_resource(Users, "/users/me", "/users")
api.add_resource(Quizzes, "/quizzes", "/quizzes/<int:quiz_id>")
api.add_resource(Subjects, "/subjects", "/subjects/<int:subject_id>")
api.add_resource(QuizSubmit, "/submit")
api.add_resource(UserScores, "/scores")
api.add_resource(Statistics, "/stats")