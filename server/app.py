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

class Users(Resource):
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


class Categories(Resource):
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
    

class Recipes(Resource):
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
        

class RecipeById(Resource):
    def get(self, id):
        recipe = Recipe.query.filter(Recipe.id == id).first()
        if recipe:
            return make_response(Recipe.to_dict(), 200)
        return make_response({'error': 'Recipe not found'}, 404)
    
    def patch(self, id):
        recipe = Recipe.query.filter(Recipe.id == id).first()
        if recipe:
            try:
                data = request.get_json()
                for attr in data:
                    setattr(recipe, attr, data[attr])
                db.session.commit()
                return make_response(recipe.to_dict(), 202)
            except ValueError:
                return make_response({'error': 'Failed to edit recipe'}, 400)
        else:
            return make_response({'error': 'recipe not found'}, 400)
        
    def delete(self, id):
        recipe = Recipe.query.filter(Recipe.id == id).first()
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            return make_response({}, 204)
        return make_response({'error':'recipe not found'}, 404)
    

class MealPlan(Resource):
    def get(self):
        meal_plans = [mp.to_dict() for mp in MealPlan.query.all()]
        return make_response(meal_plans, 200)
    
    def post(self):
        try:
            data=request.get_json()
            new_mp = MealPlan(
               date = data['date'],
               user_id = data['user_id'],
               recipe_id = data['recipe_id'], 
            )
            db.session.add(new_mp)
            db.session.commit()
            return make_response(new_mp.to_dict(), 201)
        except ValueError:
            return make_response({'error': 'unable to create new meal plan'}, 400)

class MealPlanById(Resource):
    def get(self, id):
        mp_inst = MealPlan.query.filter(MealPlan.id == id).first()
        if mp_inst:
            return make_response(mp_inst.to_dict(), 200)
        return make_response({'error': 'meal plan not found'}, 404)
    
    def patch(self, id):
        mp_inst = MealPlan.query.filter(MealPlan.id == id).first()
        if mp_inst:
            try:
                data = request.get_json()
                for attr in data:
                    setattr(mp_inst, attr, data[attr])
                db.session.commit()
                return make_response(mp_inst.to_dict(), 202)
            except ValueError:
                return make_response({'error': 'failed to edit meal plan'}, 400)
            
    def delete(self, id):
        mp_inst = MealPlan.query.filter(MealPlan.id == id).first()
        if mp_inst:
            db.session.delete(mp_inst)
            db.session.commit()
            return make_response({}, 204)
        return make_response({'error' : 'meal plan not found'}, 404)
                


api.add_resource(User, '/users')
api.add_resource(Category, '/category')
api.add_resource(Recipe, '/recipes')
api.add_resource(RecipeById, '/recipes/<int:id>')
api.add_resource(MealPlan, '/meal_plan')
api.add_resource(MealPlanById, '/meal_plan/<int:id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)

