from api.database import *
from flask_cors import CORS
from api.routes import routes
from flask import Flask, jsonify
from api.resources import api, jwt
from celery.schedules import crontab
from api.celery_init import celery_init_app
from api.tasks import compute_monthly_statistics
from flask_restful import NotFound, MethodNotAllowed
from api.config import LocalDevelopmentConfig, ProductionConfig


def create_app():
    app = Flask(__name__)
    # update app config
    if app.config.get("DEBUG"):
        app.config.from_object(LocalDevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)
    # add middlewares
    if app.config.get("DEBUG"):
        cors = CORS(app, supports_credentials=True)
    api.init_app(app)
    jwt.init_app(app)
    app.app_context().push()

    return app


# initialize the app
app = create_app()
# initialize the database
init_db(app)
# initialize celery app
celery = celery_init_app(app)
celery.autodiscover_tasks()
app.register_blueprint(routes)


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(0, 0, month_of_year='*'),
        compute_monthly_statistics.s(),
        name='update monthly statistics',
    )


@app.errorhandler(NotFound)
def handle_method_not_found(e):
    response = jsonify({"message": str(e)})
    response.status_code = 404
    return response


@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    response = jsonify({"message": str(e)})
    response.status_code = 405
    return response


if __name__ == "__main__":
    app.run()
