from flask import Flask, app
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from optparse import OptionParser # to switch between running the server and init the db
# Init app
app = Flask(__name__)
api = Api(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)


# Task db model
class TaskModel(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String(200))
    task_state = db.Column(db.String(200))


# check if task exsits
def does_task_exist(id):
    task = TaskModel.query.filter_by(task_id=id).first()
    return task


# validate state change
def does_task_state_valid(current_state, desired_state):
    if current_state == "draft" and (desired_state == "draft" or desired_state == "active" or desired_state == "archived"):
        return True
    elif current_state == "active" and (desired_state == "active" or desired_state == "done" or desired_state == "archived"):
        return True
    elif current_state == "done" and (desired_state == "done" or desired_state == "archived"):
        return True
    return False


# intialize a parser for post operation
task_post_args = reqparse.RequestParser()
# add args
task_post_args.add_argument("task_title", type=str,
                            help="Task title is required.", required=True)
task_post_args.add_argument("task_state", type=str,
                            help="Task state is required.", required=True)


# intialize a parser for update operation
task_put_args = reqparse.RequestParser()
# add args
task_put_args.add_argument("task_title", type=str)
task_put_args.add_argument("task_state", type=str)


resource_fields = {
    'task_id': fields.Integer,
    'task_title': fields.String,
    'task_state': fields.String
}


# Gel all tasks


class Tasks_list(Resource):
    @marshal_with(resource_fields)
    def get(self):
        tasks = TaskModel.query.all()
        return tasks

# for a single task


class Tasks(Resource):
    # Get single task
    @marshal_with(resource_fields)
    def get(self, id):
        task = does_task_exist(id)
        if not task:
            abort(404, message="could not find task with that id")
        return task

    # create a single task
    @marshal_with(resource_fields)
    def post(self, id):
        # parse args to dictionary
        args = task_post_args.parse_args()
        task = does_task_exist(id)
        if task:
            abort(409, message="Task ID already taken")
        new_task = TaskModel(
            task_id=id, task_title=args['task_title'], task_state=args['task_state'])
        db.session.add(new_task)
        db.session.commit()
        return new_task, 201

    # update a single task
    @marshal_with(resource_fields)
    def put(self, id):
        args = task_put_args.parse_args()
        task = does_task_exist(id)
        if not task:
            abort(404, message="Task doesn't exist, can't update.")
        if args['task_title']:
            task.task_title = args['task_title']

        if args['task_state']:
            if not does_task_state_valid(task.task_state, args['task_state']):
                abort(
                    409, message=f"cannot change from {task.task_state} state to {args['task_state']} state ")

            task.task_state = args['task_state']

        db.session.commit()
        return task

    # Delete single task
    def delete(self, id):
        task = does_task_exist(id)
        if not task:
            abort(404, message="Task doesn't exist, can't delete.")

        db.session.delete(task)
        db.session.commit()
        return "", 204


api.add_resource(Tasks_list, '/tasks')  # endpoint to get all tasks
api.add_resource(Tasks, '/tasks/<int:id>')  # endpoint to a single task


def start():
    parser = OptionParser()
    parser.add_option("-r", "--run",
                        help="Run API (Developement Server)",
                        action="store_true", dest="run")

    parser.add_option("-i", "--init",
                        help="Initialize the application (first use)",
                        action="store_true", dest="init")
                        
    (options, args) = parser.parse_args()

    # run the server
    if options.run is True:
        app.run(host="0.0.0.0",port=5000)
        print("Starting the Development HTTP server..")

    elif options.init is True:
        print("Creating database..")
        db.create_all()
    else:
        parser.print_help()


if __name__ == '__main__':
    start()
    
