from fabric.operations import local
from fabric.api import task

@task
def runserver():
    local('python manage.py runserver')