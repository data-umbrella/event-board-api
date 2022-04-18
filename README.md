# event-board
Data Umbrella: Community Events Board

# Overview

This service implements a basic REST API that leverages the Django REST Framework.

# Dependencies

- asgiref
- dj-database-url
- Django
- django-environ
- djangorestframework1
- gunicorn0
- psycopg2-binary
- sqlparse

# API Interface

```
GET /api/v1/events  
GET /api/v1/events/ID
POST /api/v1/events
PUT /api/v1/events/ID
DELETE /api/v1/events/ID
```

# Getting started with local development

Note: These instructions should work on most Linux/Unix based machines. Local development assumes you have a Python 3 installed on your computer.

1. Clone the git repository

  ```
  git clone git@github.com:data-umbrella/event-board.git
  cd event-board
  ```

2. Set up environment variable file

  ```
  cp .env.example .env
  ```

3. Set up python environment

  ```
  mkdir ~/.venvs
  python3 -m venv ~/.venvs/django-env
  ```

4. Activate python environment

  ```
  source ~/.venvs/django-env/bin/activate
  ```

5. Install dependencies

  ```
  pip install -r requirements.txt
  ```

6. Migrate database

  ```
  python manage.py migrate
  ```

7. Create a admin user

  ```
  python manage.py createsuperuser --email example@example.com --username admin
  ```

8. Run development server

  ```
  python manage.py runserver
  ```

9. Visit http://localhost:8000/admin in your browser to login into admin panel.

10. Visit http://localhost:8000/api/v1 to view Django REST framework's graphical interface.

# Contributing

1. Fork the repository by visiting https://github.com/specollective/event-board-api and clicking the **Fork** button in the top-right corner of the page. This action will create new copy of event-board-api repo under your GitHub user account generating a URL in the form https://github.com/<GITHUB_USERNAME>/event-board-api.

2. Clone the forked version of the repository.

```
git clone https://github.com/<YourUserName>/event-board-api
cd event-board-api
```

3. Add remove upstream

```
git remote add upstream https://github.com/specollective/event-board-api
```

4. Checkout a feature branch

```
git checkout -b <GITHUB_USERNAME>/<FEATURE_NAME>
```

5. Commit changes

```
echo "Example change" > example.txt
git add example.txt
git commit -m "Add example change"
```

6. Push changes to your forked repository.

```
git push -u origin new-branch-name
```

7. Compare & pull request

Visit https://github.com/specollective/event-board-api and a notification to **Compare & pull request** should be visible at the top of the repository. If you wait a little while the notification may disappear. You can also find your branch from the branch drop down and visit a link that should look like https://github.com/specollective/event-board-api/tree/new-branch-name. From there you can click the **Contribute** dropdown button which will the **Open Pull Request** for the branch. Once you've open a pull request this repo's maintainers will review your contribution. The repo's maintainers will merge it if it is looks good, or they may ask you to make some changes.

# Testing

The application currently uses Django's out-of-the-box testing environment. You can run all tests using the manage.py comment.

  ```
  python manage.py test
  ```

# Continuous Integration

The application's tests are run via Github Actions for all new branches and pull requests. The configs for the test workflow can be found in [.github/workflows/test.yaml](https://github.com/specollective/event-board-api/blob/main/.github/workflows/test.yaml).

# Deployment

This respository is configured to be easily deployed on [DigitalOceans App Platform](https://www.digitalocean.com/products/app-platform). If you want to deploy your own instance of the event board API you will want to create a new Github repository under your account, clone the repo, and change its remote origin.

  ```
  git clone git@github.com:specollective/event-board-api.git
  cd event-board-api
  git remote set-url origin https://github.com/<GITHUB_USERNAME>/event-board-api.git
  ```

Once you have your own version of the event-board-api push up to Github you can follow the step by step instructions from Digital Ocean's tutorial on how to deploy Django applications to App Platform. https://docs.digitalocean.com/tutorials/app-deploy-django-app. You will be able to connect to your Github to your Digital Ocean account. From there DigitalOcean will detect that your project is a Django app and will automatically repopulate a partial run command. The linked tutorial provides the additional configurations needed to deploy your app.
