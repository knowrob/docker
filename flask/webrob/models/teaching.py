
from webrob.app_and_db import db
from webrob.app_and_db import app
from sqlalchemy import func

class Course(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    term = db.Column(db.String(50))
    university = db.Column(db.String(50))

class CourseExercise(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey('course.id', ondelete='CASCADE'))
    number = db.Column(db.Integer())
    title = db.Column(db.String(50))
    archive = db.Column(db.LargeBinary())

class CourseTask(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    exercise_id = db.Column(db.Integer(), db.ForeignKey('course_exercise.id', ondelete='CASCADE'))
    number = db.Column(db.Integer())
    title = db.Column(db.String(50))
    text = db.Column(db.String(), nullable=False)
    
def find_courses(course):
    if course==None or course=='': return []
    # TODO: fuzzymatch using levenshtein distance
    #    Use (somehow): func.levenshtein(text_field, match_text) \in R
    return Course.query.filter(
      func.lower(Course.name).like(func.lower('%'+course+'%'))
    ).all()

def get_exercises(course_id):
    return CourseExercise.query.filter_by(course_id=course_id).all()

def get_tasks(exercise_id):
    return CourseTask.query.filter_by(exercise_id=exercise_id).all()

def get_task(exercise_id, task_number):
    return CourseTask.query.filter_by(exercise_id=exercise_id, number=task_number).first()
