from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session
from flask_app.models import user
import re 
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


class Show:
    db = "shows"
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.users = None



#Create
    @classmethod
    def create_report(cls, data):
        if not cls.validate_show(data):
            return False
        query = """
        INSERT INTO shows ( title, network, release_date, content, users_id )
        VALUES ( %(title)s, %(network)s, %(release_date)s, %(content)s, %(users_id)s)
        ;"""
        show_id = connectToMySQL(cls.db).query_db(query, data)
        return show_id




# Read SQL
    @classmethod
    def get_show_by_id(cls, id):
        data = {'id' : id}
        query = """
        SELECT *
        FROM shows
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result


    @classmethod
    def get_all_shows(cls):
        query = """
        SELECT *
        FROM shows
        LEFT JOIN users
        ON users_id = users.id
        ;"""
        result = connectToMySQL(cls.db).query_db(query)
        shows = []
        for row in result:
            show = cls(row)
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            show.users = user.User(user_data)
            shows.append(show)
        return shows

    @classmethod
    def get_one_show(cls, id):
        data = {
            "id" : id
        }
        query = """
        SELECT *
        FROM shows
        LEFT JOIN users
        ON users_id = users.id
        WHERE shows.id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        show = cls(results[0])
        user_data = {
            'id' : results[0]['users.id'],
            'first_name' :results[0]['first_name'],
            'last_name' :results[0]['last_name'],
            'email' : results[0]['email'],
            'password' :results[0]['password'],
            'created_at' :results[0]['users.created_at'],
            'updated_at' :results[0]['users.updated_at']
        }
        show.users = user.User(user_data)
        return show


#update  
    @classmethod
    def update(cls, data):
        if not cls.validate_show(data):
            return False
        query = """
        UPDATE shows 
        SET title=%(title)s, network=%(network)s, release_date=%(release_date)s, content=%(content)s 
        WHERE id=%(id)s
        ;"""
        return connectToMySQL(cls.db).query_db( query, data )




#DELETE 

    @classmethod
    def delete_show(cls, id):
        data = {'id': id}
        query = "DELETE FROM shows WHERE id=%(id)s;"
        connectToMySQL(cls.db).query_db(query,data)






# STATIC METHODS VALIDATION 
    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show['title']) < 3 :
            flash(' Title field is required  must be at least 3 characters long')
            is_valid = False
        if len(show['network']) < 3 :
            flash(' Network field is required  must be at least 3 characters long')
            is_valid = False
        if len(show['release_date']) < 3 :
            flash('Release Date field is required')
            is_valid = False
        if len(show['content']) < 3 :
            flash('Content field is required  must be at least 3 characters long')
            is_valid = False
        return is_valid