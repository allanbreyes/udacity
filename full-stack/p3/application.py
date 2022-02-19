import os
from flask import Flask, flash, g, jsonify, redirect, render_template,\
                  request, session, url_for
from flask.ext.github import GitHub
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# set-up github oauth - https://github-flask.readthedocs.org/en/latest/
if os.environ.has_key('GITHUB_CLIENT_ID') and\
   os.environ.has_key('GITHUB_CLIENT_SECRET'):
    # set app configuration variables to environment variables
    app.config['GITHUB_CLIENT_ID'] = os.environ['GITHUB_CLIENT_ID']
    app.config['GITHUB_CLIENT_SECRET'] = os.environ['GITHUB_CLIENT_SECRET']
else:
    # set to None if they're not available
    app.config['GITHUB_CLIENT_ID'] = None
    app.config['GITHUB_CLIENT_SECRET'] = None
github = GitHub(app)

from database_setup import Base, User, Provider, Course
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

if True: #os.environ['APP_SETTINGS'] == "config.DevelopmentConfig":
    engine = create_engine(os.environ['DATABASE_URL'])
    Base.metadata.bind = engine

    DBSession = scoped_session(sessionmaker(bind=engine))
    db_session = DBSession()

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    db_session = SQLAlchemy(app)

repo_uri = 'https://github.com/allanbreyes/mooc-catalog'
base_uri = '/catalog/'
api_uri = base_uri + 'api/'

# oauth
@app.route('/login')
def login():
    """ login route/routine """
    if app.config['GITHUB_CLIENT_ID'] and app.config['GITHUB_CLIENT_SECRET']:
        return github.authorize(redirect_uri=url_for('authorized', _external=True))
    else:
        flash('Howdy, developer! If you downloaded this, you still have to obtain a GitHub API client ID and key to get it wired up and working.', 'warning')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """ logout route/routine """
    session.pop('user_id', None)
    session.pop('user_token', None)
    flash('You\'ve been successfully logged out... mortal.', 'success')
    return redirect(url_for('index'))

@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    """ callback from github oauth """
    next_url = request.args.get('next')
    if oauth_token is None:
        flash('Authorization failed.', 'danger')
        return redirect(next_url)

    user = db_session.query(User).filter_by(access_token=oauth_token).first()
    if user is None:
        user = User(oauth_token)
        db_session.add(user)

    # store access token into database
    user.access_token = oauth_token
    db_session.commit()

    # store user id and access token in session hash
    session['user_id'] = user.id
    session['user_token'] = user.access_token

    flash('You\'re logged in!  Now you have incredible superpowers...', 'success')
    return redirect(url_for('index'))

# helper functions
def base_query():
    """ returns the full list of providers and courses """
    providers = db_session.query(Provider).all()
    courses = db_session.query(Course).all()
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
    try:
        start_date = datetime.strptime(form['course-start-date'][0], '%Y-%m-%d')
    except ValueError as e:
        start_date = datetime.now()
        flash('You didn\'t enter a valid date (how\'d you manage that, anyway?). I picked today. Yay!', 'warning')
    course = Course(name=form['course-name'][0],
                    course_url=form['course-url'][0],
                    thumbnail_url=form['course-thumbnail-url'][0],
                    course_number=form['course-number'][0],
                    description=form['course-description'][0],
                    start_date=start_date,
                    featured=form['course-featured'][0],
                    provider_id=form['course-provider'][0])
    return course

def authenticated():
    """ returns whether or not the session user is authenticated """
    if session.has_key('user_id') and session.has_key('user_token'):
        user = db_session.query(User).filter_by(id=session['user_id']).first()
        if user:
            return user.access_token == session['user_token']
    return False

def can_edit(course):
    """ returns whether the course is owned by the session user """
    if authenticated():
        if course.adder_id == None:
            return False
        else:
            return session.has_key('user_id') and course.adder_id == session['user_id']
    else:
        return False

# routes
@app.route('/source')
def source():
    """ redirects to github repository """
    return redirect(repo_uri)

@app.route(base_uri+'seed')
def seed_database(fixture_filename='fixtures.json'):
    """ seed route, used to populate an empty database,
    this should only have to run the first time. """
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
            db_session.add(provider)
        # TODO: implement postgresql compatibility with seeded courses (reverse id
        #       lookup on course provider)
        # seed_courses = fixtures['courses']
        # for c in seed_courses:
        #     course = Course(name=c['name'],
        #                     course_url=c['course_url'],
        #                     thumbnail_url=c['thumbnail_url'],
        #                     course_number=c['course_number'],
        #                     description=c['description'],
        #                     start_date=datetime.strptime(c['start_date'], '%Y-%m-%d'),
        #                     featured=c['featured'],
        #                     provider_id=c['provider_id'])
        #     db_session.add(course)
        try:
            db_session.commit()
            flash('Database seeded with fixture data.', 'warning')
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
    featured_courses = db_session.query(Course).filter_by(featured=True).order_by(Course.start_date)
    return render_template('index_courses.html',
                           providers=providers, courses=featured_courses,
                           title='Featured Courses', title_link=None,
                           logged_in=authenticated, editable=can_edit)

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

@app.route(api_uri+'providers', methods=['GET'])
def index_providers_api():
    """ returns JSON response of providers """
    providers, _ = base_query()
    return jsonify(providers=[p.serialize for p in providers])

@app.route(api_uri+'providers/<int:provider_id>', methods=['GET'])
def index_courses_api(provider_id):
    """ returns JSON response of courses """
    provider_courses = db_session.query(Course).filter_by(provider_id=provider_id).order_by(Course.start_date)
    return jsonify(courses=[pc.serialize for pc in provider_courses])

@app.route(base_uri+'providers/<int:provider_id>', methods=['GET'])
def index_courses(provider_id):
    """ provider show screen / courses index screen """
    providers, _ = base_query()
    try:
        provider = db_session.query(Provider).filter_by(id=provider_id).one()
    except:
        flash('Could not find what you were looking for :(', 'danger')
        return redirect(url_for('index'))
    provider_courses = db_session.query(Course).filter_by(provider_id=provider_id).order_by(Course.start_date)
    return render_template('index_courses.html',
                           providers=providers, courses=provider_courses,
                           title=provider.name, title_link=provider.homepage_url,
                           logged_in=authenticated, editable=can_edit)

@app.route(base_uri+'courses/<int:course_id>', methods=['GET'])
def view_course(course_id):
    """ course view screen """
    providers, _ = base_query()
    try:
        course = db_session.query(Course).filter_by(id=course_id).one()
    except:
        flash('Could not find what you were looking for :(', 'danger')
        return redirect(url_for('index'))
    return render_template('view_course.html',
                           providers=providers, course=course,
                           title=course.name,
                           logged_in=authenticated,
                           editable=can_edit)

@app.route(base_uri+'courses/new', methods=['GET', 'POST'])
def new_course():
    """ handles new course creation """
    if not authenticated():
        return redirect(url_for('login'))
    providers, _ = base_query()
    if request.method == 'POST':
        course = parse_course_form(request.form)
        course.adder_id = session['user_id']
        db_session.add(course)
        try:
            db_session.commit()
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
                               logged_in=authenticated)

@app.route(base_uri+'courses/<int:course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id):
    """ handles course editing """
    providers, _ = base_query()
    course = db_session.query(Course).filter_by(id=course_id).one()
    if not authenticated():
        return redirect(url_for('login'))
    elif not can_edit(course):
        flash('You don\'t own this! (Can\'t touch this, dun nan nan na... na na... na na.)', 'warning')
        return redirect(url_for('view_course', course_id=course_id))
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
        db_session.add(course)
        try:
            db_session.commit()
            flash('Changes saved!', 'success')
        except Exception as e:
            flash('Something imploded. {}'.format(e), 'danger')
        return redirect(url_for('view_course', course_id=course_id))
    else:
        return render_template('edit_course.html',
                               providers=providers, course=course,
                               title='Editing: ' + course.name,
                               form_action=url_for('edit_course', course_id=course_id),
                               logged_in=authenticated)

@app.route(base_uri+'courses/<int:course_id>/delete', methods=['GET', 'POST'])
def delete_course(course_id):
    """ handles course deletion """
    providers, _ = base_query()
    course = db_session.query(Course).filter_by(id=course_id).one()
    if not authenticated():
        return redirect(url_for('login'))
    elif not can_edit(course):
        flash('What are you doing here?', 'warning')
        return redirect(url_for('view_course', course_id=course_id))
    if request.method == 'POST':
        provider = db_session.query(Provider).filter_by(id=course.provider_id).one()
        db_session.delete(course)
        try:
            db_session.commit()
            flash('Course was deleted... forevarrrrrrrr!', 'success')
            return redirect(url_for('index_courses', provider_id=provider.id))
        except Exception as e:
            flash('Something imploded. {}'.format(e), 'danger')
            return redirect(url_for('view_course', course_id=course.id))
    return render_template('delete_course.html',
                           providers=providers, course=course,
                           title='Are you sure that you want to DELETE:',
                           form_action=url_for('delete_course', course_id=course_id),
                           logged_in=authenticated)

if __name__ == '__main__':
    app.debug = True;
    app.run(host='0.0.0.0', port=5000)
