
import os
from sqlalchemy import Column, String, Integer
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import json
import babel

local_database = "postgresql://uri:2@localhost:5432/heroes"
database_path = os.environ.get('DATABASE_URL', local_database)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
moment = Moment(app)


'''
Associating Table for Teams and Members
'''
teams_members = db.Table('team_members',
                         db.Column('team_id',
                                   db.Integer,
                                   db.ForeignKey('teams.id'),
                                   primary_key=True),
                         db.Column('hero_id',
                                   db.Integer,
                                   db.ForeignKey('heroes.id'),
                                   primary_key=True))

'''
Hero

'''


class Hero(db.Model):
    __tablename__ = 'heroes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    secret_identity = Column(String)
    hometown = Column(String)
    power_level = Column(Integer)
    teams = db.relationship('Team', secondary=teams_members,
                            back_populates='members')

    def __init__(self, name, secret_identity, hometown, power_level):
        self.name = name
        self.secret_identity = secret_identity
        self.hometown = hometown
        self.power_level = power_level

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
            'name': self.name,
            'secret_identity': self.secret_identity,
            'hometown': self.hometown,
            'power_level': self.power_level,
            'team_memberships': [team.name for team in self.teams]
        }


'''
Team

'''


class Team(db.Model):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    members = db.relationship('Hero', secondary=teams_members,
                              back_populates='teams')

    def __init__(self, name, location):
        self.name = name
        self.location = location

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
            'name': self.name,
            'location': self.location,
            'members': [member.name for member in self.members]
        }
