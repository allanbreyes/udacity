from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Mooc, Course

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

base_uri = '/catalog/'

@app.route('/catalog')
@app.route('/')
def index():
    return 'index feed'

@app.route(base_uri+'moocs/new', methods=['GET', 'POST'])
def new_mooc():
    return 'new mooc'

@app.route(base_uri+'moocs/<int:mooc_id>/edit', methods=['GET', 'POST'])
def edit_mooc(mooc_id):
    return 'edit mooc #{}'.format(mooc_id)

@app.route(base_uri+'moocs/<int:mooc_id>/delete', methods=['GET', 'POST'])
def delete_mooc(mooc_id):
    return 'delete mooc #{}'.format(mooc_id)

@app.route(base_uri+'moocs/<int:mooc_id>', methods=['GET'])
def index_courses(mooc_id):
    return 'catalog for mooc #{}'.format(mooc_id)

@app.route(base_uri+'courses/<int:course_id>', methods=['GET'])
def view_course(course_id):
    return 'view course #{}'.format(course_id)

@app.route(base_uri+'courses/new', methods=['GET', 'POST'])
def new_course():
    return 'new course'

@app.route(base_uri+'courses/<int:course_id>/edit', methods = ['GET', 'POST'])
def edit_course(course_id):
    return 'edit course #{0}'.format(course_id)

@app.route(base_uri+'courses/<int:course_id>/delete', methods = ['GET', 'POST'])
def delete_course(course_id):
    return 'delete course #{0}'.format(course_id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
