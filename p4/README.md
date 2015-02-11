# Conference Organization App API Project

### About

This project is a cloud-based API server to support a web-based and native Android application for conference organization.  The API supports the following functionality:

- User authentication (via Google accounts)
- User profiles
- Conference information
- Session information
- User wishlists

The API is hosted on Google App Engine as application ID [full-stack-conference](https://full-stack-conference.appspot.com), and can be accessed via the [API explorer](https://apis-explorer.appspot.com/apis-explorer/?base=https://full-stack-conference.appspot.com/_ah/api#p/).

### Design and Improvement Tasks

#### Task 1: Add Sessions to a Conference

I added the following endpoint methods:

- `createSession`: given a conference, creates a session.
- `getConferenceSessions`: given a conference, returns all sessions.
- `getConferenceSessionsByType`: given a conference and session type, returns all applicable sessions.
- `getSessionsBySpeaker`: given a speaker, returns all sessions across all conferences.

For the `Speaker` model design, I implemented the following datastore properties:

| Property        | Type             |
|-----------------|------------------|
| name            | string, required |
| highlights      | string           |
| speaker         | string, required |
| duration        | integer          |
| typeOfSession   | string, repeated |
| date            | date             |
| startTime       | time             |
| organizerUserId | string           |

In order to represent the one `conference` to many `sessions` relationship, I opted to use a parent-child implementation.  This allows for strong consistent querying, as sessions can be queried by their conference ancestor.  While this remits the possibility to move sessions between conferences, I reasoned that the trade-off in speed and consistency was worthwhile.  People would want to know (i.e. query) about sessions quite often.  Furthermore, sessions were `Memcached` to reflect that load.

In representing speakers, I contemplated linking the speaker field to user profiles.  However, I decided against this, as it would force a speaker to have an account, to be registered.  The obvious drawback here, though, is that querying by speaker could produce undesirable results with inconsistent entry, e.g. "John Bravo, Johnny Bravo, J. Bravo" would all be listed as separate speakers.

Session types (e.g. talk, lecture) were implemented more in a "tag" representation, with sessions able to receive multiple different types.

#### Task 2: Add Sessions to User Wishlist

I modified the `Profile` model to accommodate a 'wishlist' stored as a repeated key property field, named `sessionsToAttend`.  In order to interact with this model in the API, I also had modify some of the previous methods in Task 1 to return a unique web-safe key for sessions.  I added two endpoint methods to the API:

- `addSessionToWishlist`: given a session websafe key, saves a session to a user's wishlist.
- `getSessionsInWishlist`: return a user's wishlist.

#### Task 3: Indexes and Queries

`NotImplemented`

#### Task 4: Add Featured Speaker

`NotImplemented`

### Setup Instructions

To deploy this API server locally, ensure that you have downloaded and installed the [Google App Engine SDK for Python](https://cloud.google.com/appengine/downloads). Once installed, conduct the following steps:

1. Clone this repository. Only the `p4` directory is essential to this project.
2. (Optional) Update the value of `application` in `app.yaml` to the app ID you have registered in the App Engine admin console and would like to use to host your instance of this sample.
3. (Optional) Update the values at the top of `settings.py` to reflect the respective client IDs you have registered in the [Developer Console][4].
4. (Optional) Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
5. (Optional) Mark the configuration files as unchanged as follows: `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
6. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080][5].)
7. (Optional) Generate your client library(ies) with [the endpoints tool][6].
8. (Optional) Deploy the application via `appcfg.py update`.

### Resources

- [Google App Engine Python Docs](https://cloud.google.com/appengine/docs/python/)
- [Programming Google App Engine (Book)](http://www.amazon.com/Programming-Google-App-Engine-Sanderson/dp/144939826X)
- [Data Modeling for Google App Engine Using Python and ndb (Screencast)](https://www.youtube.com/watch?v=xZsxWn58pS0)
- [App Engine Modeling: Parent-Child Models (GitHub)](https://github.com/GoogleCloudPlatform/appengine-modeling-ndb/blob/master/parent_child_models.py)