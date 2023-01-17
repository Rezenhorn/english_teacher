# :mortar_board: Your Perfect Tutor - English Teacher project
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/downloads/release/python-379/) [![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) [![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/) [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/) [![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/) [![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org/) [![Workflow](https://github.com/Rezenhorn/english_teacher/actions/workflows/main.yml/badge.svg)](https://github.com/Rezenhorn/english_teacher/actions/workflows/nain.yml)

## :page_with_curl: Description:

A website for an English tutor that has the function of a business card and also:
- User registration
- Handing out homework to students
- Tracking learning progress
- Creating of a personal dictionary with the translation of words, the ability to download a dictionary in the excel format, etc.

## :hammer_and_wrench: Techs:
- Python 3.7.9
- Django 3.2.16
- PostgreSQL
- Testing with Django unit tests
- Bootstrap 5
- Docker, docker-compose, nginx and gunicorn
- CI/CD using GitHub Actions

## :computer: How to run the project on your computer:

### Clone the repository:
```
git clone https://github.com/Rezenhorn/english_teacher.git
```
### Create file .env in directory infra/ and fill it in according to the example (file .env.example).
### Make sure, that Docker is installed on your system and launched. From directory infra/ start Docker:
```
docker-compose up -d --build
```
### Apply migrations, create superuser, collect static:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
## If you want to stop running containers:
```
docker-compose down -v
```

## 👨‍💻 Author:

- [Dmitry Fomichev](https://github.com/Rezenhorn)