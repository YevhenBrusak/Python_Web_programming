from flask_restful import Resource, reqparse, fields, marshal_with
from flask import jsonify
from . import task_api_bp, api
from ..to_do.models import Task, Priority, Progress
from ..import db
import datetime


parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('description')
parser.add_argument('deadline')
parser.add_argument('priority')
parser.add_argument('category_id')
parser.add_argument('progress')
parser.add_argument('owner_id')

product_fields = {
    'id' : fields.Integer,
    'title' : fields.String,
    'description': fields.String,
    'priority' : fields.String,
    'progress' : fields.String,
    'created' : fields.String,
    'deadline' : fields.DateTime,
    'owner_id' : fields.Integer

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
        title = data['title']
        description = data['description']
        deadline = datetime.datetime.strptime(data['deadline'], '%Y-%m-%d')
        priority = Priority(int(data['priority']))
        progress = Progress(int(data['progress']))
        category = data['category_id']
        new_task = Task(title=title, 
                        description=description,
                        priority=priority,
                        progress = progress,
                        deadline = deadline,
                        category_id=category,
                        owner_id=data.get('owner_id')) 
        
        db.session.add(new_task)
        db.session.commit()
        
        task = Task.query.filter_by(title=title).first()
        
        return task, 201

    @marshal_with(product_fields)
    def put(self, todo_id):
        data = parser.parse_args()
        
        task = Task.query.get_or_404(todo_id)
        if data.get('title'):
            task.title = data.get('title')
        if data.get('description'):
            task.description = data.get('description')
        if data.get('deadline'):
            task.deadline = datetime.datetime.strptime(data['deadline'], '%Y-%m-%d')
        if data.get('priority'):
            task.priority = Priority(int(data.get('priority')))
        if data.get('progress'):
            task.priority = Progress(int(data.get('progress')))
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
            return jsonify({'message': 'Error has occured!'})
        
        return jsonify({'message': 'The task has been deleted!'})
        
api.add_resource(TaskApi, '/<string:todo_id>', '/')