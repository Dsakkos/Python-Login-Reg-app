from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session
from flask_app.models import show
import re 
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class User:
    db = "shows"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.shows = []

#CREATE USER 
    @classmethod
    def create_user(cls, data):
        if not cls.validate_user_reg_data(data):
            return False
        data = cls.parse_registration_data(data)
        query = """
        INSERT INTO users ( first_name , last_name , email, password )
        VALUES ( %(first_name)s , %(last_name)s , %(email)s, %(password)s)
        ;"""
        users_id = connectToMySQL(cls.db).query_db(query, data)
        session['users_id'] = users_id
        return users_id



# * GET USER BY ID
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db( query, data)
        return cls(results[0])



#GET USER
    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email}
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s
        ;"""
        results = connectToMySQL(cls.db).query_db( query, data)
        if results:
            results = cls(results[0])
        return results



#STATIC METHODS VALIDATION 
    @staticmethod
    def validate_user_reg_data(registration_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if not EMAIL_REGEX.match(registration_data['email']):
            flash('Email is not a valid email address')
            is_valid = False
        if len(registration_data['first_name']) < 3 :
            flash('First name must be at least 2 characters')
            is_valid = False
        if len(registration_data['last_name']) < 3 :
            flash('Last name must be at least 2 characters')
            is_valid = False
        if len(registration_data['password']) < 8 :
            flash('Password must be at least 8 characters')
            is_valid = False
        if User.get_user_by_email(registration_data['email'].lower()):
            flash('Email is already registered')
            is_valid = False
        if registration_data['password'] != registration_data['confirm_password']:
            flash(' Your password does not match the password you entered')
            is_valid = False
        return is_valid


#PARSE DATA 
    @staticmethod
    def parse_registration_data(data):
        parsed_data = {
        'email' : data['email'].lower(),
        'password' : bcrypt.generate_password_hash(data['password']),
        'first_name' : data['first_name'],
        'last_name' : data['last_name'],
        }
        return parsed_data


#Login User 
    @staticmethod
    def login(data):
        user = User.get_user_by_email(data['email'].lower())
        if user:
            if bcrypt.check_password_hash(user.password, data['password']):
                session['users_id'] = user.id
                return True
        flash('Incorrect Login Try Again!!')
        return False







