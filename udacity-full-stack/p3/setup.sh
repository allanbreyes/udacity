# development/localhost
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="sqlite:///catalog.db"
export GITHUB_CLIENT_ID=63af9832f4ddc627f1bc
export GITHUB_CLIENT_SECRET=030eaa097a85af3e691156476d52fe29d4fa0bfa

# production/heroku
heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro
heroku config:set GITHUB_CLIENT_ID=###
heroku config:set GITHUB_CLIENT_SECRET=###

# production/apache2
export DATABASE_URL="postgresql://localhost/catalog"