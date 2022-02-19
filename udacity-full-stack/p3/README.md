# Item Catalog: The MOOC Catalog

by Allan Reyes, in fulfillment of Udacity's [Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/nd004)

### About

This application provides a list of items (MOOCs) within a variety of categories (MOOC providers) and provides a user registration and authentication system.  Registered users (anyone with a GitHub account) will have the ability to post, edit and delete their own items.

### How to run

This simple web application uses GitHub for authorization and authentication.  To simulate security best practices, the API keys are not in the main application file or hard-coded.  However, to facilitate grading, a shell script, `export_keys.sh`, is available to export API keys (current as of the time of submission) to server environment variables.

This repository contains the `mooc-catalog` submodule, provisioned as `catalog`. The more updated and application-only code (no vagrant configuration) can be found at the [mooc-catalog](https://github.com/allanbreyes/mooc-catalog) repository.

To spin this website up:

1. Download or clone the `p3/vagrant` directory.
2. Initialize the Vagrant vm via `vagrant up`, which should set up on `localhost:5000`.
3. Connect to the virtual machine: `vagrant ssh`.
4. (Optional) Obtain your own GitHub API keys by [registering a new application](https://github.com/settings/applications).  Ensure you add `localhost:5000/github-callback` as the authorization callback URL.
5. (Optional) Inside the virtual machine, `export` your own API keys, `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`.
6. Navigate to the catalog directory: `cd /vagrant/catalog`
7. (Optional) Run the provided key export shell script: `source ../export_keys.sh`.
8. Start the server: `python application.py`.
9. Navigate to it in your browser of choice at `localhost:5000`.  The first-time run of the server will initialize the database with fixture data.
10. Let me know of any bugs :P