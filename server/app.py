#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, session 
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import User, Category, Recipe, MealPlan

# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

class User(Resource):
    def get(self):
        users = [user.to_dict(rules=('-meal_plans',)) for user in User.query.all()]
        return make_response(users,200)
    
    def post(self):
        try:
            data= request.get_json()
            new_user = User(
                name=data['name']
            )
            db.session.add(new_user)
            db.session.commit()
            return make_response(new_user.to_dict('-meal_plans',), 201)
        except ValueError:
            return make_response({'error': 'Failed to add a new user, try again'}, 400)


class Category(Resource):
    def get(self):
        categories = [category.to_dict() for category in Category.query.all()]
        return make_response(categories, 200)
    
    def post(self):
        try:
            data = request.get_json()
            new_category = Category(
                name = data['name']
                )
            db.session.add(new_category)
            db.session.commit()
            return make_response(new_category.to_dict(), 201)
        except ValueError:
            return make_response({'error': 'Failed to add new category'}, 404)
    

class Recipe(Resource):
    def get(self):
        recipes = [recipes.to_dict() for recipe in Recipe.query.all()]
        return make_response(recipes, 200)
    
    def post(self):
        try:
            data = request.get_json()
            new_recipe = Recipe(
                name=data['name'],
                ingredients=data['ingredients'],
                directions=data['directions'],
                category_id=data['category_id']
            )
            db.session.add(new_recipe)
            db.session.commit()
            return make_response(new_recipe.to_dict(), 201)
        except ValueError:
            return make_response({'error': 'Failed to add new recipe'}, 400)
        
api.add_resource(Recipe, '/recipes')
api.add_resource(Category, '/category')
api.add_resource(User, '/users')




if __name__ == '__main__':
    app.run(port=5555, debug=True)

