from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Provider, Course
from datetime import datetime

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

base_uri = '/catalog/'

# helper functions
def base_query():
    providers = session.query(Provider).all()
    courses = session.query(Course).all()
    return providers, courses

def get_by_id(id, items):
    """ returns an item in a list of items where item['id'] == id """
    for item in items:
        if id == item.id:
            return item
    raise LookupError('id {} not found'.format(id))

# routes
@app.route(base_uri+'seed')
def seed_database(fixture_filename='fixtures.json'):
    providers, _ = base_query()
    if len(providers) != 0:
        flash_message = 'Database is not empty.'
    else:
        import json
        with open(fixture_filename, 'rb') as f:
            fixtures = json.load(f)
        seed_providers = fixtures['providers']
        for p in seed_providers:
            provider = Provider(name=p['name'], homepage_url=p['homepage_url'])
            session.add(provider)
        seed_courses = fixtures['courses']
        for c in seed_courses:
            course = Course(name=c['name'],
                            course_url=c['course_url'],
                            thumbnail_url=c['thumbnail_url'],
                            course_number=c['course_number'],
                            description=c['description'],
                            start_date=datetime.strptime(c['start_date'], '%Y-%m-%d'),
                            featured=c['featured'],
                            provider_id=c['provider_id'])
            session.add(course)
        session.commit()
        flash_message = 'Database seeded with fixture data.'
    return redirect(url_for('index'))

@app.route('/catalog')
@app.route('/')
def index():
    seed_database()
    providers, courses = base_query()
    featured_courses = [course for course in courses if course.featured]
    return render_template('index_courses.html',
                           providers=providers, courses=featured_courses,
                           title='Featured Courses', title_link=None,
                           logged_in=True)

# @app.route(base_uri+'providers/new', methods=['GET', 'POST'])
# def new_provider():
#     providers, courses = base_query()
#     return 'new provider'

# @app.route(base_uri+'providers/<int:provider_id>/edit', methods=['GET', 'POST'])
# def edit_provider(provider_id):
#     providers, courses = base_query()
#     return 'edit provider #{}'.format(provider_id)

# @app.route(base_uri+'providers/<int:provider_id>/delete', methods=['GET', 'POST'])
# def delete_provider(provider_id):
#     providers, courses = base_query()
#     return 'delete provider #{}'.format(provider_id)

@app.route(base_uri+'providers/<int:provider_id>', methods=['GET'])
def index_courses(provider_id):
    providers, courses = base_query()
    try:
        provider = get_by_id(provider_id, providers)
    except LookupError:
        flash_message = NotImplemented
        return redirect(url_for('index'))
    provider_courses = [course for course in courses if course.provider_id == provider_id]
    return render_template('index_courses.html',
                           providers=providers, courses=provider_courses,
                           title=provider.name, title_link=provider.homepage_url,
                           logged_in=True)

@app.route(base_uri+'courses/<int:course_id>', methods=['GET'])
def view_course(course_id):
    providers, courses = base_query()
    try:
        course = get_by_id(course_id, courses)
    except LookupError:
        flash_message = NotImplemented
        return redirect(url_for('index'))
    return render_template('view_course.html',
                           providers=providers, course=course,
                           title=course.name,
                           logged_in=True)

@app.route(base_uri+'courses/new', methods=['GET', 'POST'])
def new_course():
    providers, _ = base_query()
    if request.method == 'POST':
        flash_message = NotImplemented
        return redirect(url_for('index'))
    else:
        course = {"id": None, "name": "", "course_url": "", "thumbnail_url": "",
                  "course_number": "", "description": "", "perpetual": False,
                  "start_date": "", "featured": False, "provider_id": None}
        return render_template('edit_course.html',
                               providers=providers, course=course,
                               title='New Course',
                               form_action=url_for('new_course'),
                               logged_in=True)

@app.route(base_uri+'courses/<int:course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id):
    providers, courses = base_query()
    course = get_by_id(course_id, courses)
    if request.method == 'POST':
        flash_message = NotImplemented
        return redirect(url_for('view_course', course_id=course_id))
    else:
        return render_template('edit_course.html',
                               providers=providers, course=course,
                               title='Editing: ' + course.name,
                               form_action=url_for('edit_course', course_id=course_id),
                               logged_in=True)

@app.route(base_uri+'courses/<int:course_id>/delete', methods=['GET', 'POST'])
def delete_course(course_id):
    providers, courses = base_query()
    course = get_by_id(course_id, courses)
    if request.method == 'POST':
        provider = get_by_id(course.provider_id, providers)
        flash_message = NotImplemented
        return redirect(url_for('index_courses', provider_id=provider.id))
    return render_template('delete_course.html',
                           providers=providers, course=course,
                           title='Are you sure that you want to DELETE:',
                           form_action=url_for('delete_course', course_id=course_id),
                           logged_in=True)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
