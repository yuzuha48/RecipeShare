from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user 
from flask_app import app
from flask import flash
import os
import uuid

class Recipe:
    DB = "recipes_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.photo = data["photo"]
        self.description = data["description"]
        self.ingredients = data["ingredients"]
        self.instructions = data["instructions"]
        self.cook_time = data["cook_time"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None

    @classmethod
    def get_one(cls, recipe_id):
        data = {"id": recipe_id}
        query = """
                SELECT * FROM recipes 
                JOIN users ON users.id = recipes.users_id
                WHERE recipes.id=%(id)s;
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        one_recipe = cls(results[0])
        for row in results:
            data = {
                "id": row["users.id"],
                "first_name": row["first_name"], 
                "last_name": row["last_name"], 
                "email": row["email"], 
                "password": row["password"], 
                "created_at": row["users.created_at"], 
                "updated_at": row["users.updated_at"]
            }
        one_recipe.user = user.User(data)
        return one_recipe

    @classmethod
    def get_all(cls):
        query = """ SELECT * FROM recipes 
                JOIN users ON users.id = recipes.users_id
                """
        results = connectToMySQL(cls.DB).query_db(query)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)
            user_data = {
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_recipe.user = user.User(user_data)
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def save(cls, recipe_data, photo, user_id):

        file_ext = os.path.splitext(photo.filename)[1]
        random_string = uuid.uuid4().hex
        unique_filename = random_string + file_ext
        photo.save(os.path.join(app.config["UPLOAD_DIR"], unique_filename))

        data = {
            "name": recipe_data["name"], 
            "photo": unique_filename,
            "description": recipe_data['description'], 
            "ingredients": recipe_data['ingredients'], 
            "instructions": recipe_data['instructions'], 
            "cook_time": recipe_data['cook_time'],
            "users_id": user_id
        }
        query = """
                INSERT INTO recipes (name, photo, description, ingredients, instructions, cook_time, users_id) 
                VALUES (%(name)s, %(photo)s, %(description)s, %(ingredients)s, %(instructions)s, %(cook_time)s, %(users_id)s);
                """
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_recipe(data, photo):
        is_valid = True 
        if len(data['name']) < 3 or len(data['description']) < 3  or len(data['ingredients']) < 3 or len(data['instructions']) < 3:
            flash("Name, description, and/or instructions must be at least 3 characters.", "create")
            is_valid = False 
        if not data['cook_time'] or int(data['cook_time']) < 1:
            flash("Please enter a valid cook time.", "create")
            is_valid = False
        if not photo:
            flash("Recipe must have a photo.", "create")
            is_valid = False
        return is_valid

    @classmethod
    def edit(cls, recipe_id, recipe_data, photo):
        file_ext = os.path.splitext(photo.filename)[1]
        random_string = uuid.uuid4().hex
        unique_filename = random_string + file_ext
        photo.save( os.path.join(app.config["UPLOAD_DIR"], unique_filename))

        data = {
            "id": recipe_id,
            "name": recipe_data['name'],
            "photo": unique_filename,
            "description": recipe_data['description'],
            "ingredients": recipe_data['ingredients'],
            "instructions": recipe_data['instructions'], 
            "cook_time": recipe_data["cook_time"]
        }
        query = """
                UPDATE recipes
                SET name=%(name)s, photo=%(photo)s, description=%(description)s, ingredients=%(ingredients)s, instructions=%(instructions)s, cook_time=%(cook_time)s
                WHERE id=%(id)s;
                """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete(cls, recipe_id):
        data = {"id": recipe_id}
        query = "DELETE FROM recipes WHERE id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)