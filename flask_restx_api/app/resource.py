from flask_restx import Namespace, Resource
from .api_models import course_model, student_model, course_input_model, student_input_model
from .models import Course, Student
from .extensions import db

ns = Namespace('api', description='API namespace')

@ns.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    
@ns.route("/courses")
class CoursesAPI(Resource):
    @ns.marshal_list_with(course_model)
    def get(self):

        # Get all courses
        return Course.query.all()

    @ns.expect(course_input_model)
    @ns.marshal_with(course_model)
    def post(self):
        print(ns.payload)
        course = Course(name=ns.payload["name"])
        db.session.add(course)
        db.session.commit()
        return course, 201

@ns.route("/students")
class StudentsAPI(Resource):
    @ns.marshal_list_with(student_model)
    def get(self):
        # Get all students
        return Student.query.all()
   
    @ns.expect(student_input_model)
    @ns.marshal_with(student_model)
    def post(self):
        print(ns.payload)
        student = Student(name=ns.payload["name"], course_id=ns.payload["course_id"])
        db.session.add(student)
        db.session.commit()
        return student, 201
    
@ns.route("/courses/<int:id>")
class CourseAPI(Resource):
    @ns.marshal_with(course_model)
    def get(self, id):
        # Get course by id
        return Course.query.get(id)
    
    def delete(self, id):
        # Delete course by id
        course = Course.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return '', 204

@ns.route("/students/<int:id>")
class StudentAPI(Resource):
    @ns.marshal_with(student_model)
    def get(self, id):
        # Get student by id
        return Student.query.get(id)
    
    @ns.expect(student_input_model)
    @ns.marshal_with(student_model)
    def put(self, id):
        # Update student by id
        student = Student.query.get(id)
        student.name = ns.payload["name"]
        student.course_id = ns.payload["course_id"]
        db.session.commit()
        return student, 200
    
    def delete(self, id):
        # Delete student by id
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()
        return '', 204