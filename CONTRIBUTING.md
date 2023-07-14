# Contributing to the Data Umbrella Events Board

## About
This event board application is built with [ReactJS](https://reactjs.org/) and bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

There are two parts:  
1. front-end: [event-board-web](https://github.com/data-umbrella/event-board-web) repository; [CONTRIBUTING.md](https://github.com/data-umbrella/event-board-web/blob/main/CONTRIBUTING.md)
1. back-end: [event-board-api](https://github.com/data-umbrella/event-board-api) repository; [CONTRIBUTING.md](https://github.com/data-umbrella/event-board-api/blob/main/CONTRIBUTING.md)

## Overview

This service implements a basic REST API that leverages the Django REST Framework.

## Development Dependencies

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Docker Compose

## Python Dependencies

- asgiref
- dj-database-url
- Django
- django-environ
- djangorestframework1
- gunicorn0
- psycopg2-binary
- sqlparse

## API Interfaces

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
Note: You will want to create a project folder and clone both the "event-board-web" and "event-board-api" repositories in to that folder.

Suggested folder name:  du-event-board
  ```console
  mkdir du-event-board
  cd du-event-board
  ```

  ```console
  git clone git@github.com:data-umbrella/event-board-api.git
  ```
  
  Go into the repository:  
  ```console
  cd event-board-api
  ```

### 2. Build the docker images

  ```console
  docker compose build
  ```

Note: Docker (desktop) should be running before `docker compose build`. Otherwise you will see this message.
```console
▶ docker compose build
[+] Building 0.0s (0/0)                                                                                                      
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
(base) 
```

### 3. Start the web server and database

  ```console
  docker compose up
  ```

  The command for starting the web service migrates the database for you running executing following commands before starting the web server. See the `docker-compose.yml` file for details.
  
  ```console
  docker compose run web python manage.py seed
  ```
  ```console
  docker compose run web python manage.py makemigrations
  ```
  ```console
  docker compose run web python manage.py migrate
  ```
  ```console
  docker compose run web python manage.py runserver 0.0.0.0:8000
  ```

  The first time running `docker compose up` you may run into an issue with the web server timing out waiting for the database to initialize. You may need to run `docker compose down` and running `docker compose up` again or starting the services separately.

  ```console
  docker compose up db
  ```
  ```console
  docker compose up web
  ```

### 4. Create admin user

  ```console
  docker compose run web python manage.py createsuperuser --email example@example.com
  ```

### 5. Open the admin console in the browser

Visit http://localhost:8000/admin in your browser to login into admin panel.

### 6. View the Django REST framework's graphical interface for the events API

Visit the http://localhost:8000/api/v1/events to view the API documentation site.

### 7. Running tests

  ```console
  docker-compose run web python manage.py test
  ```

# Contributing

### 1. Checkout a feature branch

```console
git checkout -b <GITHUB_USERNAME>/<FEATURE_NAME>
```

### 2. Commit changes

```console
echo "Example change" > example.txt
```
```console
git add example.txt
```
```console
git commit -m "Add example change"
```

### 3. Push changes to your forked repository

```console
git push -u origin new-branch-name
```

### 4. Open a pull request

When you push up a new branch to GitHub a link to directly open a pull request is printed to the console. You can also visit https://github.com/specollective/event-board-api and a notification to **Compare & pull request** should be visible at the top of the repository. If you wait a little while the notification may disappear. You can also find your branch from the branch drop down and visit a link that should look like https://github.com/specollective/event-board-api/tree/new-branch-name. From there you can click the **Contribute** dropdown button which will the **Open Pull Request** for the branch. Once you've open a pull request this repo's maintainers will review your contribution. The repo's maintainers will merge it if it is looks good, or they may ask you to make some changes.

# Testing

The application currently uses Django's out-of-the-box testing environment. You can run all tests using the manage.py comment.

  ```console
  docker compose up python manage.py test
  ```

# Continuous Integration

The application's tests are run via GitHub Actions for all new branches and pull requests. The configs for the test workflow can be found in [.github/workflows/test.yaml](https://github.com/specollective/event-board-api/blob/main/.github/workflows/test.yaml).

# Deployment

The Data Events Board is deployed on [DigitalOceans App Platform](https://www.digitalocean.com/products/app-platform). Digital Ocean (DO) connects to the GitHub and on initialization detects that the repository is a Django project and automatically populates default configuration. The project is configured to parameterize the settings for the project using encrypted environment variables set in DO. To learn more deploying Django apps on Digital Ocean (DO) App see their tutorial https://docs.digitalocean.com/tutorials/app-deploy-django-app.


---

## Video resources

This is a playlist of 3 videos, [Intro to React Tutorial](https://www.youtube.com/playlist?list=PLBKcU7Ik-ir9bAT2eXmQ4Ojn2--hT3O87):  
1. React Tutorial Part 1: [Background](https://youtu.be/jNO-pPR7zkg)
1. React Tutorial Part 2: [JavaScript, Node.js](https://youtu.be/JWt4Z4sAlxk)
1. React Tutorial Part 3: [React Fundamentals, Build Your First React Front-end Application](https://youtu.be/MSAbOBHGkhw)

This is a playlist of 3 videos, [Intro to Django](https://www.youtube.com/playlist?list=PLBKcU7Ik-ir9HhpZQr3WolhYgbqtZSJZr):  
1. Django Tutorial Part 1: [Python for Beginners](https://youtu.be/Yr1ewxg8os8)
1. Django Tutorial Part 2: [Intro to Web Development Frameworks](https://youtu.be/K4NQmrGEWGM)
1. Django Tutorial Part 3: [Building Your First Django Application](https://www.youtube.com/watch?v=QTQSzirDs8E&list=PLBKcU7Ik-ir9HhpZQr3WolhYgbqtZSJZr&index=3&t=1s)

### Resources
- [Django REST Framework](https://www.django-rest-framework.org/)

---

## Contributing guidelines

1) To claim an issue, "I am working on it" and then you can start working on it; there is no need to wait to be assigned on an issue.
2) A pull request should be submitted within two weeks or someone else can work on the issue.


## Thank you
Thank you for contributing to the Data Umbrella Events Board.
