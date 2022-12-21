from flask_restful import Resource, reqparse, fields, marshal_with
from flask import jsonify
from . import task_api_bp, api
from ..to_do.models import Task, Priority
from ..import db


parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('description', type=str)
parser.add_argument('priority', type=str)
parser.add_argument('category_id', type=int)
parser.add_argument('owner_id', type=int)

task_update = reqparse.RequestParser()
task_update.add_argument('title', type=str)
task_update.add_argument('description', type=str)
task_update.add_argument('priority', type=str)
task_update.add_argument('category_id', type=int)
task_update.add_argument('owner_id', type=int)


product_fields = {
    'id' : fields.Integer,
    'title' : fields.String,
    'description': fields.String,
    'priority' : fields.String,
    'progress' : fields.String,
    'created' : fields.String,
    'deadline' : fields.String,
}


class TaskApi(Resource):
    @marshal_with(product_fields)
    def get(self, todo_id=None):   
          
        if todo_id is None:
            tasks = Task.query.all()           
            return tasks
       
        task = Task.query.get_or_404(todo_id)  
        return task, 201
    
    
    @marshal_with(product_fields)
    def post(self):
        data = parser.parse_args()
        
        new_task = Task(title=data['title'], 
                        description=data['description'],
                        priority=Priority(int(data.get('priority'))),
                        category_id=data.get('category_id'),
                        owner_id=data.get('owner_id')) 
        
        db.session.add(new_task)
        db.session.commit()
        
        task = Task.query.all()[-1]
        
        return task, 201

    @marshal_with(product_fields)
    def put(self, todo_id):
        data = task_update.parse_args()
        
        task = Task.query.get_or_404(todo_id)
        if data.get('title'):
            task.title = data.get('title')
        if data.get('description'):
            task.description = data.get('description')
        if data.get('priority'):
            task.priority = Priority(int(data.get('priority')))
        if data.get('category_id'):
            task.category_id = data.get('category_id')
        if data.get('owner_id'):
            task.owner_id = data.get('owner_id')
            
        db.session.commit()        
        task = Task.query.get_or_404(todo_id)  
        return task
    
    def delete(self, todo_id):
        task = Task.query.get_or_404(todo_id)
        
        try:
            db.session.delete(task)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({'message': 'Error has occured!!!'})
        
        return jsonify({'message': 'The post has been deleted!'})
        
    

api.add_resource(TaskApi, '/<string:todo_id>', '/')