""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'drivers'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _email = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, email, password):
        self._name = name    # variables with self prefix become part of the object, 
        self._email = email
        self._password = password

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def email(self):
        return self._email
    
    # a setter function, allows name to be updated after initial object creation
    @email.setter
    def email(self, email):
        self._email = email
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    @property
    def password(self):
        return self._password
    
    # setter method for password
    @password.setter
    def password(self, password):
        self._password = password
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "name" : self.name,
            "email" : self.email,
            "password" : self.password,
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", email="", password=""):
        """only updates values with length"""
        if len(name) > 0:
            self._name = name
            self._email = email
        if len(password) > 0:
            self._password = password
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    u1 = User(name='Ryan McWeeny', email='ryanrob327@gmail.com', password='Password')
    u2 = User(name='Aragorn', email='ranger123@gmail.com', password='Password2')
    u3 = User(name='Gandolf', email='wizard456@gmail.com', password='Password3')
    u4 = User(name='Sauron', email='evilEye789@gmail.com', password='Password4')
    u5 = User(name='Frodo Baggins', email='hobbit1011@TheShire.com', password='Password5')
    u6 = User(name='Gimbli', email='Dwarf@gmail.com', password='Password6')
    
    users = [u1, u2, u3, u4, u5, u6]
    
            
    for user in users:
        try:
            user.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {user.uid}")