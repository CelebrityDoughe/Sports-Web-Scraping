# -*- coding: utf-8 -*-
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Date

from .settings import (
    MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB_HOST,
    MYSQL_DB_PORT, MYSQL_DB_NAME
)


Base = declarative_base()


class Team(Base):
    __tablename__ = 'teams_team'

    id = Column(Integer, primary_key=True)
    url = Column(String(200), unique=True)
    name = Column(String(128))

    def __repr__(self):
        return '<Team(%s)>' % self.name


class Schedule(Base):
    __tablename__ = 'schedules_schedule'

    id = Column(Integer, primary_key=True)
    team = Column('team_id', Integer, ForeignKey('teams_team.id'))
    opponent = Column('opponent_id', Integer, ForeignKey('teams_team.id'))
    date = Column(Date)
    matchup_url = Column(String(200))
    location = Column(String(16))
    score = Column(Integer, nullable=True)
    opponent_score = Column(Integer, nullable=True)
    score_result = Column(Integer, nullable=True)
    result = Column(String(32))
    status = Column(String(16))


class Stats(Base):
    __tablename__ = 'stats_stats'

    id = Column(Integer, primary_key=True)
    schedule = Column('schedule_id', Integer, ForeignKey('schedules_schedule.id'))
    category = Column(String(32))
    data = Column(String)


engine = create_engine(
    'mysql://%s:%s@%s:%s/%s?charset=utf8' % (
    MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB_HOST, MYSQL_DB_PORT, MYSQL_DB_NAME))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def get_all_teams():
    return session.query(Team).all()


def get_team_by_url(team_url):
    return session.query(Team).filter(Team.url==team_url).first()


def get_schedule(team, date):
    return session.query(Schedule).filter(Schedule.team==team).filter(Schedule.date==date).first()


def get_schedule_by_id(schedule_id):
    return session.query(Schedule).filter(Schedule.id==schedule_id).first()


def get_all_schedules():
    return session.query(Schedule).all()


def get_stats(schedule_id, category):
    return session.query(Stats).filter(Stats.schedule==schedule_id).filter(Stats.category==category).first()
