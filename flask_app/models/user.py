from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

class User:
    DB = "recipes_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recipes = []

    @classmethod
    def save(cls, user_data):
        pw_hash = bcrypt.generate_password_hash(user_data['password'])
        data = {
            "first_name": user_data["first_name"], 
            "last_name": user_data["last_name"],
            "email": user_data["email"], 
            "password": pw_hash
        }
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(cls.DB).query_db(query, data)
        user_info = User.get_one(result)
        return user_info

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data["first_name"]) < 2 or len(data["last_name"]) < 2:
            flash("First name and/or last name must be at least 2 characters.", "registration")
            is_valid = False
        if data["first_name"].isalpha() == False or data["last_name"].isalpha()== False:
            flash("First name and/or last name may only contain letters.", "registration")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Email address is invalid.", "registration")
            is_valid = False

        if User.get_by_email(data):
            flash("Email is associated with an existing user.", "registration")
            is_valid = False
        if len(data["password"]) < 8:
            flash("Password must be at least 8 characters.", "registration")
            is_valid = False
        if any(char.isdigit() for char in data['password']) == False:
            flash("Password must contain at least one number.", "registration")
            is_valid = False
        if data['password'].islower() == True:
            flash("Password must contain at least one capital letter.", "registration")
            is_valid = False
        if data["confirm_password"] != data["password"]:
            flash("Passwords do not match.", "registration")
            is_valid = False

        return is_valid

    @classmethod
    def get_one(cls, user_id):
        data = {"id": user_id}
        query = "SELECT * FROM users WHERE id=%(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return cls(result[0])

    @classmethod
    def get_all(cls):
        query = """
                    SELECT * from users 
                """
        results = connectToMySQL(cls.DB).query_db(query)

        all_users = []
        for one_user in results:
            all_users.append(cls(one_user))
        return all_users

    @classmethod 
    def get_by_email(cls, user_data):
        data = {"email": user_data["email"]}
        query = "SELECT * FROM users WHERE email=%(email)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False 
        return cls(result[0])   