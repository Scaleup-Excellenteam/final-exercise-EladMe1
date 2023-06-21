from datetime import datetime
import uuid

from sqlalchemy import ForeignKey, Integer, String, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
        User model representing a user in the system.
        """
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String, unique=True, nullable=False)
    uploads = relationship('Upload', cascade='all, delete-orphan')


class Upload(Base):
    """
        Upload model representing a file upload.
        """
    __tablename__ = 'uploads'

    id = mapped_column(Integer, primary_key=True)
    uid = mapped_column(String, nullable=False)
    filename = mapped_column(String, nullable=False)
    upload_time = mapped_column(DateTime, nullable=False)
    finish_time = mapped_column(DateTime)
    status = mapped_column(String)
    user_id = mapped_column(Integer, ForeignKey('users.id'), default="empty", nullable=False)

    user = relationship('User', back_populates='uploads')

    def __init__(self, filename: str, status: str, uidFile: str, user_id: int = None):
        self.uid = str(uuid.uuid4())
        self.filename = filename
        self.upload_time = datetime.now()
        self.status = status
        self.user_id = user_id
        self.uid = uidFile

    def upload_path(self) -> str:
        """
               Returns the upload path of the file.
               """
        return f'/uploads/{self.uid}/{self.filename}'

    def set_finish_time(self):
        """
                Sets the finish time of the upload to the current datetime.
                """
        self.finish_time = datetime.now()

    def set_status(self, status: str):
        """
               Sets the status of the upload.

               Args:
                   status (str): The status of the upload.
               """
        self.status = status

    def add_error_message(self, error_message: str):
        """
              Adds an error message to the upload.

              Args:
                  error_message (str): The error message to add.
              """
        pass


# Create a session to interact with the database
engine = create_engine('sqlite:///db/database.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create the database and tables
Base.metadata.create_all(engine)


