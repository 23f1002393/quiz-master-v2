import os
from sqlalchemy import select
from datetime import datetime
from api.database import session
from api.models import User, Quiz, Score
from sqlalchemy.exc import IntegrityError
from api.tasks import compute_monthly_statistics, compute_user_statistics
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, send_from_directory, make_response, jsonify, Blueprint
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    current_user
)


routes = Blueprint('routes', __name__)


@routes.route('/', methods=('GET',))
def index():
    return send_from_directory('static', 'index.html', mimetype='text/html')


@routes.route('/api/login', methods=('POST',))
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if user := session.execute(select(User).where(User.email == email)).scalar():
        if check_password_hash(user.password, password):
            response = make_response({
                "id": user.id,
                "name": user.name,
                "isAdmin": user.email == 'admin@qm.xyz'
            })

            access_token = create_access_token(identity=user)
            set_access_cookies(response, access_token)
            return response
        return make_response('invalid credentials', 401)
    return make_response('failed to login user', 404)


@routes.route('/api/users/me', methods=('GET',))
@jwt_required()
def get_user():
    return jsonify(current_user=dict(
        id=current_user.id,
        name=current_user.name,
        isAdmin=current_user.email == 'admin@qm.xyz'
    ))


@routes.route('/api/register', methods=('POST',))
def register():
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
        return make_response('user created successfully', 201)
    except IntegrityError:
        return make_response('user already exists', 400)


@routes.route('/api/logout', methods=('GET',))
def logout():
    response = make_response('user logged out', 200)
    unset_jwt_cookies(response)
    return response


@routes.route('/api/quiz/<int:quiz_id>/submit', methods=('POST',))
@jwt_required()
def submit_quiz(quiz_id):
    try:
        payload = request.get_json()
        quiz = session.execute(select(Quiz).where(
            Quiz.id == quiz_id)).scalar()

        user_score = 0
        for question in quiz.questions:
            if question.correct == payload["selected"][str(question.id)]:
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


@routes.route('/api/user/stats', methods=('GET',))
@jwt_required()
def user_stats():
    result = compute_user_statistics.delay(dict(
        email=current_user.email,
        scores=[dict(
            subject=score.quiz.subject.name,
            date_of_quiz=score.quiz.date_of_quiz,
            user_score=score.user_score,
            total_score=score.total_score,
        ) for score in current_user.scores],
    ))
    while not result.ready():
        pass
    [by_subject, by_month] = result.get()
    return jsonify({
        "by_subject": by_subject,
        "by_month": by_month
    })


@routes.route('/api/admin/stats', methods=('GET',))
@jwt_required()
def admin_stats():
    by_month = "admin_month_wise.png"
    by_subject = "admin_subject_wise.png"

    compute_monthly_statistics.delay()

    return make_response({
        "by_subject": by_subject,
        "by_month": by_month
    }, 200)
