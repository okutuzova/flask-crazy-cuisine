from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'
db = SQLAlchemy(app)


class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<Recipe %r>" % self.id


@app.route("/recipes/")
def recipes():
    all_recipes = Recipe.query.all()
    return render_template("recipes.html", recipes=all_recipes)



@app.route("/recipes/delete/<int:id>/")
def delete(id):
    recipe = Recipe.query.get_or_404(id)
    try:
        db.session.delete(recipe)
        db.session.commit()
        return redirect("/recipes")
    except:
        return "An error occured when deleting a recipe"


@app.route("/recipes/edit/<int:id>/", methods=["GET", "POST"])
def edit(id):
    recipe = Recipe.query.get_or_404(id)
    if request.method == 'POST':
        recipe.title = request.form['title']
        recipe.description = request.form['description']
        try:
            db.session.commit()
            return redirect('/recipes')
        except:
            return "Error while updating a recipe"
    else:
        return render_template("edit.html", recipe=recipe)




@app.route("/home/<string:name>/")
def hello(name):
    return f"Hello, Culinar {name}!"


@app.route("/")
@app.route("/home/")
def home():
    num_recipes = Recipe.query.count()
    return render_template('index.html', num_recipes=num_recipes)


@app.route("/recipes/new/", methods=["GET", "POST"])
def new_recipe():
    if request.method == 'POST':
        recipe_title = request.form['title']
        recipe_description = request.form['description']
        new_myrecipe = Recipe(title=recipe_title, description=recipe_description, author="Olga")
        db.session.add(new_myrecipe)
        try:
            db.session.commit()
            return redirect('/recipes')
        except:
            return "An error occured when adding a new recipe."

    else:
        return render_template("new_recipe.html")



if __name__ == '__main__':
    app.run(debug=True)
