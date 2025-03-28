import os
from flask import Config
from secrets import token_urlsafe


class AppConfig(Config):
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", token_urlsafe())
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_ACCESS_CSRF_HEADER_NAME = 'X-CSRF-TOKEN'
    JWT_ACCESS_CSRF_FIELD_NAME = 'csrf_access_token'
    CELERY = {
        'broker_url': 'redis://localhost',
        'result_backend': 'redis://localhost',
        'task_ignore_result': False
    }


class LocalDevelopmentConfig(AppConfig):
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False


class ProductionConfig(AppConfig):
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = False
