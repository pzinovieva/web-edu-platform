import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Course(SqlAlchemyBase):
    __tablename__ = 'courses'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date_str = sqlalchemy.Column(sqlalchemy.String, default=f"{datetime.datetime.now():%d-%m-%Y}")
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = sqlalchemy.orm.relation('User')


class Lesson(SqlAlchemyBase):
    __tablename__ = 'lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    content = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    link_video = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content_homework = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    created_date_str = sqlalchemy.Column(sqlalchemy.String, default=f"{datetime.datetime.now():%d-%m-%Y}")
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    course_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("courses.id"))
    course = sqlalchemy.orm.relation('Course')


class Review(SqlAlchemyBase):
    __tablename__ = 'review_courses'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    created_date_str = sqlalchemy.Column(sqlalchemy.String, default=f"{datetime.datetime.now():%d-%m-%Y}")
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    course_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("courses.id"))
    course = sqlalchemy.orm.relation('Course')
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = sqlalchemy.orm.relation('User')
