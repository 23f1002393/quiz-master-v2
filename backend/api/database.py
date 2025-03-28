from api.models import *
from sqlalchemy import create_engine, select
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine('sqlite:///quiz-master.db')
session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine))


def init_db(app):
    Base.metadata.create_all(bind=engine)

    with app.app_context():
        if not session.execute(select(User).where(User.email == 'admin@qm.xyz')).scalar():
            session.add(User(
                email="admin@qm.xyz",
                name="admin",
                password=generate_password_hash("admin"),
                qualification='Senior Secondary',
                dob=date(2004, 5, 8)))
            session.commit()

    app.teardown_appcontext(lambda _: session.close())
