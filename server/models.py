from sqlalchemy_serializer import SerializerMixin
# from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

from config import db

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    # 'meal_plans' is the correct relationship for User, not 'recipes'.
    meal_plans = db.relationship('MealPlan', back_populates='user', cascade='all, delete')

    serialize_rules = ('-meal_plans.user',)

    def __repr__(self):
        return f'<User {self.id}: {self.name}>'

class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    recipes = db.relationship('Recipe', back_populates='category', cascade='all, delete')

    serialize_rules = ('-recipes.category',)

    def __repr__(self):
        return f'<Category {self.id}: {self.name}>'

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    directions = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    # The relationship needs to match the 'recipes' back_populates in Category.
    category = relationship('Category', back_populates='recipes')
    # 'meal_plans' is the correct relationship for Recipe.
    meal_plans = db.relationship('MealPlan', back_populates='recipe', cascade='all, delete')

    serialize_rules = ('-meal_plans.recipe', '-category.recipes',)

    def __repr__(self):
        return f'<Recipe {self.id}: {self.name}, {self.ingredients}, {self.directions}>'

class MealPlan(db.Model, SerializerMixin):
    __tablename__ = 'meal_plans'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

    user = relationship('User', back_populates='meal_plans')
    recipe = relationship('Recipe', back_populates='meal_plans')

    serialize_rules = ('-user.meal_plans', '-recipe.meal_plans')

    def __repr__(self):
        return f'<MealPlan {self.id}>'