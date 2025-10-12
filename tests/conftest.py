import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.tasks.models import Task

User = get_user_model()


@pytest.fixture
def password():
    return "P@ssw0rd12345"


@pytest.fixture
def user(db, password):
    return User.objects.create_user(username="alice", password=password, 
                                    first_name="Alice", last_name="A")


@pytest.fixture
def other_user(db, password):
    return User.objects.create_user(username="bob", password=password, 
                                    first_name="Bob", last_name="B")


@pytest.fixture
def auth_client(db, user, password):
    c = Client()
    c.login(username=user.username, password=password)
    return c


@pytest.fixture
def status_new(db):
    return Status.objects.create(name="новый")


@pytest.fixture
def label_bug(db):
    return Label.objects.create(name="bug")


@pytest.fixture
def make_task(db, status_new, user):
    def _make_task(**kwargs):
        defaults = {
            "name": "Test task",
            "description": "",
            "status": status_new,
            "author": user,
            "executor": None,
        }
        defaults.update(kwargs)
        return Task.objects.create(**defaults)
    return _make_task
