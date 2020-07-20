import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)



@app.route('/',methods=['POST'])
@requires_auth('post:drinks')
def headers(payload):
    print(payload)
    return 'Access Granted'





'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks',methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    drinks = [drink.short() for drink in drinks]
    return jsonify({
        "success":True,
        "drinks":drinks
        }),200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>',methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload,id):
    drink = Drink.query.get_or_404(id)
    return jsonify({
        "success":True,
        "drinks":drink.short()
        }),200


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks',methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    r = request.get_json()
    title = r.get('title',None)
    recipe = r.get('recipe',None)
    
    
    # if request dosen't contain title or recipe then it's bad request
    if(not (title and recipe)  ):
        abort(400)

    # if found another drink then raise 422 error because title must be unique
    drink = Drink.query.filter(Drink.title == title).one_or_none() 

    if(drink):
        abort(422,f"{title} already exists")


    try:
        drink = Drink()
        drink.title = title
        drink.recipe = json.dumps(recipe)
        drink.insert()

        return jsonify({
            "success":True,
            "drink":drink.long()
        })

    except :
        abort(422,"unprocessable");


    



'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

# @app.route('/drinks',methods=['PATCH'])
# def update_drinks(payload,id):
    


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": error.description
    }), 422



'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def not_found(error):
    jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
    }), 404
'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''

# i changed autherror to abort it's status code and send it so it will be hancdeled inside the error handler
@app.errorhandler(401)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 401,
        "code": error.description['code'],
        "description": error.description['description']
    }), 401
