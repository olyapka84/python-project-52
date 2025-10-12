import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def users(db):
    pwd = "p12345678"
    u1 = User.objects.create_user(username="user1", password=pwd)
    u2 = User.objects.create_user(username="user2", password=pwd)
    return {"u1": u1, "u2": u2, "pwd": pwd}


@pytest.fixture
def auth_client(users):
    c = Client()
    c.login(username="user1", password=users["pwd"])
    return c


@pytest.fixture
def status_new(db):
    return Status.objects.create(name="новый")


def test_login_required(client):
    r = client.get(reverse("tasks:index"))
    assert r.status_code in (302, 301)


def test_list(auth_client, users, status_new):
    Task.objects.create(name="Тестовая задача", description="Описание",
                        status=status_new, author=users["u1"])
    Task.objects.create(name="Вторая", description="Ещё одна",
                        status=status_new, author=users["u1"])
    r = auth_client.get(reverse("tasks:index"))
    assert r.status_code == 200
    html = r.content.decode()
    assert "Тестовая задача" in html
    assert "Вторая" in html


def test_create(auth_client, users, status_new):
    resp = auth_client.post(reverse("tasks:create"), data={
        "name": "Новая задача",
        "description": "Что-то сделать",
        "status": status_new.pk,
        "executor": users["u2"].pk,
    })
    assert resp.status_code in (302, 301)
    assert Task.objects.filter(name="Новая задача",
                               status=status_new,
                               author=users["u1"]).exists()


def test_update(auth_client, users, status_new):
    t = Task.objects.create(name="Черновик", description="Описание",
                            status=status_new, author=users["u1"])
    resp = auth_client.post(reverse("tasks:update", args=[t.pk]), data={
        "name": "Изменено",
        "description": "Новое описание",
        "status": status_new.pk,
        "executor": users["u2"].pk,
    })
    assert resp.status_code in (302, 301)
    t.refresh_from_db()
    assert t.name == "Изменено"
    assert t.description == "Новое описание"
    assert t.executor == users["u2"]


def test_view(auth_client, users, status_new):
    t = Task.objects.create(name="Посмотреть", description="Детали",
                            status=status_new, author=users["u1"])
    r = auth_client.get(reverse("tasks:detail", args=[t.pk]))
    assert r.status_code == 200
    html = r.content.decode()
    assert "Посмотреть" in html
    assert "Детали" in html


def test_delete(auth_client, users, status_new):
    t = Task.objects.create(name="Удалить", description="Ненужная",
                            status=status_new, author=users["u1"])
    r_get = auth_client.get(reverse("tasks:delete", args=[t.pk]))
    assert r_get.status_code == 200
    r_post = auth_client.post(reverse("tasks:delete", args=[t.pk]))
    assert r_post.status_code in (302, 301)
    assert not Task.objects.filter(pk=t.pk).exists()


def test_only_author_can_delete(auth_client, users, status_new):
    t = Task.objects.create(
        name="Чужая задача", description="...",
        status=status_new, author=users["u2"]
    )
    r = auth_client.post(reverse("tasks:delete", args=[t.pk]))
    assert r.status_code in (302, 301)
    assert Task.objects.filter(pk=t.pk).exists()

    c = Client()
    c.login(username="user2", password=users["pwd"])
    r2 = c.post(reverse("tasks:delete", args=[t.pk]))
    assert r2.status_code in (302, 301)
    assert not Task.objects.filter(pk=t.pk).exists()
