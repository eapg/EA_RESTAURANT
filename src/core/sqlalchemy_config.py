# ORM sqlalchemy session creation

from sqlalchemy.orm import sessionmaker


def create_session(engine):
    session_creation = sessionmaker(
        bind=engine, expire_on_commit=False, autocommit=True
    )
    session = session_creation()
    return session
