from flask import Flask, flash, render_template, request, redirect,\
                  url_for, jsonify

app = Flask(__name__)
app.secret_key = "superfragilisticexpialidocious"

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
    """ returns the full list of providers and courses """
    providers = session.query(Provider).all()
    courses = session.query(Course).all()
    return providers, courses

def parse_course_form(form):
    """ returns a new Course object from submitted form data POST requests """
    form = dict(form)
    if form['course-thumbnail-url'][0] == "":
        form['course-thumbnail-url'][0] = 'http://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/MOOC_-_Massive_Open_Online_Course_logo.svg/799px-MOOC_-_Massive_Open_Online_Course_logo.svg.png'
    if not form.has_key('course-featured'):
        form['course-featured'] = [False]
    else:
        form['course-featured'] = [True]
    course = Course(name=form['course-name'][0],
                    course_url=form['course-url'][0],
                    thumbnail_url=form['course-thumbnail-url'][0],
                    course_number=form['course-number'][0],
                    description=form['course-description'][0],
                    start_date=datetime.strptime(form['course-start-date'][0],
                                                 '%Y-%m-%d'),
                    featured=form['course-featured'][0],
                    provider_id=form['course-provider'][0])
    return course

# routes
@app.route(base_uri+'seed')
def seed_database(fixture_filename='fixtures.json'):
    """ seed route, used to populate an empty database """
    providers, _ = base_query()
    if len(providers) != 0:
        pass
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
        try:
            session.commit()
            flash('Database seeded with fixture data.', 'success')
        except Exception as e:
            flash('Something imploded. {}'.format(e), 'danger')
    return redirect(url_for('index'))

@app.route('/catalog')
@app.route('/')
def index():
    """ main index page """
    # call seed function
    seed_database()
    providers, _ = base_query()
    featured_courses = session.query(Course).filter_by(featured=True).order_by(Course.start_date)
    return render_template('index_courses.html',
                           providers=providers, courses=featured_courses,
                           title='Featured Courses', title_link=None,
                           logged_in=True)

# TODO: implement administrative privileges, routes, and templates for Provider CRUD operations
# @app.route(base_uri+'providers/new', methods=['GET', 'POST'])
# def new_provider():
#     return 'new provider'
# @app.route(base_uri+'providers/<int:provider_id>/edit', methods=['GET', 'POST'])
# def edit_provider(provider_id):
#     return 'edit provider #{}'.format(provider_id)
# @app.route(base_uri+'providers/<int:provider_id>/delete', methods=['GET', 'POST'])
# def delete_provider(provider_id):
#     return 'delete provider #{}'.format(provider_id)

@app.route(base_uri+'providers/<int:provider_id>', methods=['GET'])
def index_courses(provider_id):
    """ provider show screen / courses index screen """
    providers, _ = base_query()
    try:
        provider = session.query(Provider).filter_by(id=provider_id).one()
    except:
        flash('Could not find what you were looking for :(', 'danger')
        return redirect(url_for('index'))
    provider_courses = session.query(Course).filter_by(provider_id=provider_id).order_by(Course.start_date)
    return render_template('index_courses.html',
                           providers=providers, courses=provider_courses,
                           title=provider.name, title_link=provider.homepage_url,
                           logged_in=True)

@app.route(base_uri+'courses/<int:course_id>', methods=['GET'])
def view_course(course_id):
    """ course view screen """
    providers, _ = base_query()
    try:
        course = session.query(Course).filter_by(id=course_id).one()
    except:
        flash('Could not find what you were looking for :(', 'danger')
        return redirect(url_for('index'))
    return render_template('view_course.html',
                           providers=providers, course=course,
                           title=course.name,
                           logged_in=True)

@app.route(base_uri+'courses/new', methods=['GET', 'POST'])
def new_course():
    """ handles new course creation """
    providers, _ = base_query()
    if request.method == 'POST':
        course = parse_course_form(request.form)
        session.add(course)
        try:
            session.commit()
            flash('New course created!', 'success')
            return redirect(url_for('view_course', course_id=course.id))
        except Exception as e:
            flash('Something imploded. {}'.format(e), 'danger')
            return redirect(url_for('index'))
    else:
        course = {"id": None, "name": "", "course_url": "", "thumbnail_url": "",
                  "course_number": "", "description": "", "start_date": "",
                  "featured": False, "provider_id": None}
        return render_template('edit_course.html',
                               providers=providers, course=course,
                               title='New Course',
                               form_action=url_for('new_course'),
                               logged_in=True)

@app.route(base_uri+'courses/<int:course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id):
    """ handles course editing """
    providers, _ = base_query()
    course = session.query(Course).filter_by(id=course_id).one()
    if request.method == 'POST':
        course_params = parse_course_form(request.form)
        # TODO: figure out a way to DRY this out... no bracket notation :(
        course.name = course_params.name
        course.course_url = course_params.course_url
        course.thumbnail_url = course_params.thumbnail_url
        course.course_number = course_params.course_number
        course.description = course_params.description
        course.start_date = course_params.start_date
        course.featured = course_params.featured
        course.provider_id = course_params.provider_id
        session.add(course)
        try:
            session.commit()
            flash('Changes saved!', 'success')
        except Exception as e:
            flash('Something imploded. {}'.format(e), 'danger')
        return redirect(url_for('view_course', course_id=course_id))
    else:
        return render_template('edit_course.html',
                               providers=providers, course=course,
                               title='Editing: ' + course.name,
                               form_action=url_for('edit_course', course_id=course_id),
                               logged_in=True)

@app.route(base_uri+'courses/<int:course_id>/delete', methods=['GET', 'POST'])
def delete_course(course_id):
    """ handles course deletion """
    providers, _ = base_query()
    course = session.query(Course).filter_by(id=course_id).one()
    if request.method == 'POST':
        provider = session.query(Provider).filter_by(id=course.provider_id).one()
        session.delete(course)
        try:
            session.commit()
            flash('Course was deleted... forevarrrrrrrr!', 'success')
            return redirect(url_for('index_courses', provider_id=provider.id))
        except Exception as e:
            flash('Something imploded. {}'.format(e), 'danger')
            return redirect(url_for('view_course', course_id=course.id))
    return render_template('delete_course.html',
                           providers=providers, course=course,
                           title='Are you sure that you want to DELETE:',
                           form_action=url_for('delete_course', course_id=course_id),
                           logged_in=True)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
