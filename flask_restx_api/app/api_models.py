from .extensions import api
from flask_restx import fields

# Define the Course model

course_model = api.model('Course', {
    'id': fields.Integer,
    'name': fields.String
 })

# Define the Student model

student_model = api.model('Student', {
    'id': fields.Integer,
    'name': fields.String,
    #"students": fields.List(fields.Nested(course_model))
 })

# Define the Course model

course_input_model = api.model('CourseInput', {
    'name': fields.String(required=True)
 })

# Define the Student model
student_input_model = api.model('StudentInput', {
    'name': fields.String(required=True),
    'course_id': fields.Integer(required=True)
 })
