from functools import wraps

from app.category_api import category_api_bp
from ..import db
from ..to_do.models import Category
from ..account.models import User

from sqlalchemy.exc import IntegrityError
from flask import jsonify, request, make_response
from flask_jwt_extended import create_access_token, jwt_required


api_email = 'addams@gmail.com'
api_password = 'addams123'


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_email and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message' : 'Authentication failed!'}), 403
    return decorated


@category_api_bp.route('/token',methods=['POST'])
def login_api():
    auth=request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticated':'Basic realm="Login reguired!"'})

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login reguired!"'})

    if user.verify_password(auth.password):
        token = create_access_token(identity=user.email)
        return jsonify({'token':token})
    
    return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login reguired!"'})


@category_api_bp.route('/category', methods=['GET'])
@jwt_required()
def get_categories():

    categories = Category.query.all()

    categories_list = [dict(id=category.id, name=category.name) for category in categories ]

    return jsonify({'category' : categories_list})  


@category_api_bp.route('/category', methods=['POST'])
def add_category():
    new_category_data = request.get_json()

    if not new_category_data:
        return {'message': 'No input data provided'}, 400

    name = new_category_data[0].get('name')
    if not name:
        return jsonify({'message' : 'Not key with name'}), 422
    
    category = Category.query.filter_by(name=name).first()

    if category:
        return jsonify({'message' : f'Категорія з назвою {name} існує'}), 400
    
    try:
        category_new = Category(name=name)
        db.session.add(category_new)
        db.session.commit()
    except:
        return jsonify({'message' : f'Невідома помилка на стороні сервера'}), 400
        
    category_add = Category.query.filter_by(name=name).first()

    return jsonify( {'id' : category_add.id, 'name' : category_add.name } ), 201    
    
@category_api_bp.route('/category/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get_or_404(id)

    return jsonify({'id': category.id, 'name': category.name})


@category_api_bp.route('/category/<int:id>', methods=['PUT'])
@jwt_required()
def edit_category(id):
    
    new_category_data = request.get_json()

    name = new_category_data[0].get('name')
    if not name:
        return jsonify({'message' : 'Not key with name'})
    
    category = Category.query.get(id)

    if not category:
        return jsonify({'message' : 'Нема такої категорії'}), 404

    try:
        category.name = name
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message' : 'Така категорія існує'}), 409
  
    return jsonify({'id' : id, 'name' : name})
    
@category_api_bp.route('/category/<int:id>', methods=['DELETE'])
@protected
def delete_category(id):
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'The category has been deleted!'})