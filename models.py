from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from db_alchemy import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    def __init__(self, name, email, login, password):
        self.name = name
        self.email = email
        self.login = login
        self.password = password

    def __repr__(self):
        return f"<User {self.name}>"


class EmailCredentials(Base):
    __tablename__ = 'email_credentials'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    email = Column(String(120), unique=True, nullable=False)
    login = Column(String(50), nullable=False)
    password = Column(String(120), nullable=False)
    pop_server = Column(String(120), nullable=False)
    smtp_server = Column(String(50), nullable=False)

    def __init__(self, user_id, email, login, password, pop_server, smtp_server):
        self.user_id = user_id
        self.email = email
        self.login = login
        self.password = password
        self.pop_server = pop_server
        self.smtp_server = smtp_server

    def __repr__(self):
        return f"<Email {self.email}>"


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    company = Column(String(120), nullable=True)
    position_name = Column(String(120), nullable=True)
    description = Column(String(250), nullable=True)
    contacts_ids = Column(String(120), nullable=True)
    comment = Column(String(120), nullable=True)
    creation_date = Column(String, default=datetime.utcnow())
    status = Column(Integer, nullable=True)

    def __init__(self, company, position_name, description, contacts_ids, comment, status, user_id):
        self.company = company
        self.position_name = position_name
        self.description = description
        self.contacts_ids = contacts_ids
        self.comment = comment
        self.status = status
        self.user_id = user_id

    def __repr__(self):
        return f" < Company: {self.company}  |  Position: {self.position_name}  |  Description: {self.description}  |  " \
               f"Comment: {self.comment}  |  Contacts: {self.contacts_ids}  |  Status: {self.status} > "


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vacancy_id = Column(Integer, ForeignKey('vacancy.id'))
    description = Column(String(250), nullable=True)
    event_date = Column(String, default=datetime.utcnow())
    title = Column(String(250), nullable=True)
    deadline_date = Column(String, default=datetime.utcnow())
    status = Column(Integer, nullable=True)

    def __init__(self, vacancy_id, description, event_date, title, deadline_date, status):
        self.vacancy_id = vacancy_id
        self.description = description
        self.event_date = event_date
        self.title = title
        self.deadline_date = deadline_date
        self.status = status

    def __repr__(self):
        return f" < Vacancy: {self.vacancy_id}  |  Description: {self.description}  |  Event date: {self.event_date}  |  " \
               f"Title: {self.title}  |  Deadline date: {self.deadline_date}  |  Status: {self.status} > "


class Templates(Base):
    __tablename__ = 'templates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(50), nullable=True)
    content = Column(Text, nullable=True)

    def __init__(self, user_id, name, content):
        self.user_id = user_id
        self.name = name
        self.content = content

    def __repr__(self):
        return f"<Templates {self.name}>"


class Documents(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(50), nullable=True)
    description = Column(String(250), nullable=True)
    content = Column(Text, nullable=True)

    def __init__(self, user_id, name, content, description):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.content = content

    def __repr__(self):
        return f"<Documents {self.name}>"

