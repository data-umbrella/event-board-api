# Data Umbrella Community Events Board

This repository contains the code for Data Umbrella's community event board.

# Overview

This service implements a basic REST API that leverages the Django REST Framework.

# Development Dependencies

- Docker Desktop
- Docker Compose

# Python Dependencies

- asgiref
- dj-database-url
- Django
- django-environ
- djangorestframework1
- gunicorn0
- psycopg2-binary
- sqlparse

# API Interfaces

### Events
```
GET /api/v1/events  
GET /api/v1/events/ID
POST /api/v1/events
PUT /api/v1/events/ID
DELETE /api/v1/events/ID
```

# Getting started with development

### 1. Clone the git repository

  ```
  git clone git@github.com:data-umbrella/event-board-api.git
  cd event-board-api
  ```

### 2. Build the docker images

  ```
  docker compose build
  ```

### 3. Start the web server and database

  ```
  docker compose up
  ```

  The command for starting the web service migrates the database for you running executing following commands before starting the web server. See the `docker-compose.yml` file for details.
  
  ```
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver 0.0.0.0:8000
  ```

  The first time running `docker compose up` you may run into an issue with the web server timing out waiting for the database to initialize. You may need to run `docker compose down` and running `docker compose up` again or starting the services separately.

  ```
  docker compose up up
  docker compose up web
  ```

### 4. Create admin user

  ```
  docker compose run web python manage.py createsuperuser --email example@example.com
  ```

### 5. Open the admin console in the browser

Visit http://localhost:8000/admin in your browser to login into admin panel.

### 6. View the Django REST framework's graphical interface for the events API

Visit the http://localhost:8000/api/v1/events to view the API documentation site.

### 7. Running tests

  ```
  docker-compose run web python manage.py test
  ```

# Contributing

### 1. Checkout a feature branch

```
git checkout -b <GITHUB_USERNAME>/<FEATURE_NAME>
```

### 2. Commit changes

```
echo "Example change" > example.txt
git add example.txt
git commit -m "Add example change"
```

### 3. Push changes to your forked repository.

```
git push -u origin new-branch-name
```

### 4. Open a pull request

When you push up a new branch to Github a link to directly open a pull request is printed to the console. You can also visit https://github.com/specollective/event-board-api and a notification to **Compare & pull request** should be visible at the top of the repository. If you wait a little while the notification may disappear. You can also find your branch from the branch drop down and visit a link that should look like https://github.com/specollective/event-board-api/tree/new-branch-name. From there you can click the **Contribute** dropdown button which will the **Open Pull Request** for the branch. Once you've open a pull request this repo's maintainers will review your contribution. The repo's maintainers will merge it if it is looks good, or they may ask you to make some changes.

# Testing

The application currently uses Django's out-of-the-box testing environment. You can run all tests using the manage.py comment.

  ```
  docker compose up python manage.py test
  ```

# Continuous Integration

The application's tests are run via Github Actions for all new branches and pull requests. The configs for the test workflow can be found in [.github/workflows/test.yaml](https://github.com/specollective/event-board-api/blob/main/.github/workflows/test.yaml).

# Deployment

The Data Event Board is deployed on [DigitalOceans App Platform](https://www.digitalocean.com/products/app-platform). Digital Ocean (DO) connects to the Github and on initialization detects that the repository is a Django project and automatically populates default configuration. The project is configured to parameterize the settings for the project using encrypted environment variables set in DO. To learn more deploying Django apps on Digital Ocean (DO) App see their tutorial https://docs.digitalocean.com/tutorials/app-deploy-django-app.
