from datetime import datetime
import uuid

from sqlalchemy import ForeignKey, Integer, String, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String, unique=True, nullable=False)
    uploads = relationship('Upload', cascade='all, delete-orphan')


class Upload(Base):
    __tablename__ = 'uploads'

    id = mapped_column(Integer, primary_key=True)
    uid = mapped_column(String, nullable=False)
    filename = mapped_column(String, nullable=False)
    upload_time = mapped_column(DateTime, nullable=False)
    finish_time = mapped_column(DateTime)
    status = mapped_column(String)
    user_id = mapped_column(Integer, ForeignKey('users.id'), default="empty", nullable=False)

    user = relationship('User', back_populates='uploads')

    def __init__(self, filename, status, uidFile, user_id=None):
        self.uid = str(uuid.uuid4())
        self.filename = filename
        self.upload_time = datetime.now()
        self.status = status
        self.user_id = user_id
        self.uid = uidFile

    def upload_path(self) -> str:
        return f'/uploads/{self.uid}/{self.filename}'

    def set_finish_time(self):
        self.finish_time = datetime.now()

    def set_status(self, status: str):
        self.status = status

    def add_error_message(self, error_message: str):
        pass


# Create a session to interact with the database
engine = create_engine('sqlite:///db/database.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create the database and tables
Base.metadata.create_all(engine)


