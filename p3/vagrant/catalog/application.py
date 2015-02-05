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

# load fixture data
load_fixtures = True
if load_fixtures:
    import json
    with open('fixtures.json', 'rb') as f:
        fixtures = json.load(f)
    moocs = fixtures['moocs']
    courses = fixtures['courses']

# helper functions
def get_by_id(id, items):
    """ returns an item in a list of items where item['id'] == id """
    for item in items:
        if id == item['id']:
            return item
    raise LookupError('id {} not found'.format(id))

# routes
@app.route('/catalog')
@app.route('/')
def index():
    featured_courses = [course for course in courses if course['featured']]
    return render_template('index_courses.html',
                           moocs=moocs, courses=featured_courses,
                           title='Featured Courses', title_link=None,
                           logged_in=True)

# @app.route(base_uri+'moocs/new', methods=['GET', 'POST'])
# def new_mooc():
#     return 'new mooc'

# @app.route(base_uri+'moocs/<int:mooc_id>/edit', methods=['GET', 'POST'])
# def edit_mooc(mooc_id):
#     return 'edit mooc #{}'.format(mooc_id)

# @app.route(base_uri+'moocs/<int:mooc_id>/delete', methods=['GET', 'POST'])
# def delete_mooc(mooc_id):
#     return 'delete mooc #{}'.format(mooc_id)

@app.route(base_uri+'moocs/<int:mooc_id>', methods=['GET'])
def index_courses(mooc_id):
    try:
        mooc = get_by_id(mooc_id, moocs)
    except LookupError:
        flash_message = NotImplemented
        return redirect(url_for('index'))
    mooc_courses = [course for course in courses if course['mooc_id'] == mooc_id]
    return render_template('index_courses.html',
                           moocs=moocs, courses=mooc_courses,
                           title=mooc['name'], title_link=mooc['homepage_url'],
                           logged_in=True)

@app.route(base_uri+'courses/<int:course_id>', methods=['GET'])
def view_course(course_id):
    try:
        course = get_by_id(course_id, courses)
    except LookupError:
        flash_message = NotImplemented
        return redirect(url_for('index'))
    return render_template('view_course.html',
                           moocs=moocs, course=course,
                           title=course['name'],
                           logged_in=True)

@app.route(base_uri+'courses/new', methods=['GET', 'POST'])
def new_course():
    if request.method == 'POST':
        flash_message = NotImplemented
        return redirect(url_for('index'))
    else:
        course = {"id": None, "name": "", "course_url": "", "thumbnail_url": "",
                  "course_number": "", "description": "", "perpetual": False,
                  "start_date": "", "featured": False, "mooc_id": None}
        return render_template('edit_course.html',
                               moocs=moocs, course=course,
                               title='New Course',
                               form_action=url_for('new_course'),
                               logged_in=True)

@app.route(base_uri+'courses/<int:course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id):
    if request.method == 'POST':
        flash_message = NotImplemented
        return redirect(url_for('view_course', course_id=course_id))
    else:
        course = get_by_id(course_id, courses)
        return render_template('edit_course.html',
                               moocs=moocs, course=course,
                               title='Editing: ' + course['name'],
                               form_action=url_for('edit_course', course_id=course_id),
                               logged_in=True)

@app.route(base_uri+'courses/<int:course_id>/delete', methods=['GET', 'POST'])
def delete_course(course_id):
    return 'delete course #{0}'.format(course_id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
