from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)

    meal_plans = db.relationship('MealPlan', back_populates='user', cascade='all, delete-orphan')

class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    recipes = db.relationship('Recipe', back_populates='category')

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    directions = db.Column(db.String)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='recipes')

    meal_plans = db.relationship('MealPlan', back_populates='recipe', cascade='all, delete-orphan')

class MealPlan(db.Model, SerializerMixin):
    __tablename__ = 'meal_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

    user = db.relationship('User', back_populates='meal_plans')
    recipe = db.relationship('Recipe', back_populates='meal_plans')
