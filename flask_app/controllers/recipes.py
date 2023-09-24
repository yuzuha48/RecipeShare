from flask_app import app 
from flask_app.models import user
from flask_app.models import recipe
from flask import render_template, redirect, request, session, flash, send_from_directory
import re
from flask_bcrypt import Bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

@app.route('/')
def home_page():
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    if not user.User.validate_user(request.form):
        session["first_name"] = request.form["first_name"]
        session["last_name"] = request.form["last_name"]
        session["email"] = request.form["email"]
        return redirect('/')
        
    user_info = user.User.save(request.form)
    session["user_id"] = user_info.id
    return redirect('/recipes')

@app.route('/login', methods=['POST'])
def login():
    user_in_db = user.User.get_by_email(request.form)
    if not user_in_db:
        session["login_email"] = request.form["email"]
        flash("Invalid Email.", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        session["login_email"] = request.form["email"]
        flash("Invalid Password.", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/recipes')

@app.route('/recipes')
def show_recipes():
    if 'user_id' not in session:
        return redirect('/')
    one_user = user.User.get_one(session['user_id'])
    all_recipes = recipe.Recipe.get_all()
    return render_template("recipes.html", user=one_user, all_recipes=all_recipes)

@app.route('/recipes/new')
def create_recipe_page():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("create.html")

@app.route('/recipes/new', methods=['POST'])
def create_recipe():
    if not recipe.Recipe.validate_recipe(request.form, request.files['photo']):
        session['name'] = request.form['name']
        session['description'] = request.form['description']
        session['ingredients'] = request.form['ingredients']
        session['instructions'] = request.form['instructions']
        session['cook_time'] = request.form['cook_time']
        return redirect('/recipes/new')
    user_id = session['user_id']
    recipe.Recipe.save(request.form, request.files['photo'], user_id) 
    return redirect('/recipes')

@app.route("/uploads/<filename>")
def serve_uploads(filename):
    if 'user_id' not in session:
        return redirect('/')
    return send_from_directory(app.config["UPLOAD_DIR"], filename)

@app.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    one_user = user.User.get_one(session['user_id'])
    one_recipe = recipe.Recipe.get_one(recipe_id)
    return render_template("view.html", recipe=one_recipe, user=one_user)

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe_page(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    one_recipe = recipe.Recipe.get_one(recipe_id)
    return render_template("edit.html", recipe=one_recipe)

@app.route('/recipes/edit/<int:recipe_id>', methods=['POST'])
def edit_recipe(recipe_id):
    if not recipe.Recipe.validate_recipe(request.form, request.files['photo']):
        return redirect(f'/recipes/edit/{recipe_id}')
    recipe.Recipe.edit(recipe_id, request.form, request.files['photo'])
    return redirect(f'/recipes/{recipe_id}')

@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    recipe.Recipe.delete(recipe_id)
    return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
