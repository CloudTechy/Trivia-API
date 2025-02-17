import os
from sqlalchemy import Column, ForeignKey, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from dotenv import dotenv_values

config = dotenv_values(".env")
database_name = config['database_name']
database_path = "postgresql://{}:{}@{}/{}".format(
    config['database_username'],
    config['database_password'],
    "localhost:5432", database_name)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app=app, db=db)


"""
Question

"""


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(Integer, ForeignKey('categories.id'), nullable=False)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def __repr__(self):
        return 'Question ID:{}, question:{}, answer:{}, difficulty:{}'.format(
            self.id, self.question, self.answer, self.difficulty)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }


"""
Category

"""


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    questions = db.relationship(
        'Question', backref='parentCategory', lazy=True)

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return f'Category ID: {self.id}, type: {self.type}'

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
