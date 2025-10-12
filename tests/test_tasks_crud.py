import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status

User = get_user_model()


@pytest.fixture
def status_new(db):
    return Status.objects.create(name="новый")


@pytest.fixture
def users(db):
    password = "P@ssw0rd12345"
    u1 = User.objects.create_user(
        username="alice", password=password, first_name="Alice", last_name="A"
    )
    u2 = User.objects.create_user(
        username="bob", password=password, first_name="Bob", last_name="B"
    )
    return {"alice": u1, "bob": u2, "password": password}


@pytest.fixture
def auth_client(users):
    c = Client()
    c.login(username="alice", password=users["password"])
    return c


@pytest.mark.django_db
def test_users_list_is_public(client, users):
    resp = client.get(reverse("list", current_app="users"))
    assert resp.status_code == 200
    html = resp.content.decode()
    assert "alice" in html
    assert "bob" in html


@pytest.mark.django_db
def test_registration_get(client):
    r = client.get(reverse("create", current_app="users"))
    assert r.status_code == 200
    html = r.content.decode()
    assert 'name="username"' in html
    assert 'name="password1"' in html
    assert 'name="password2"' in html


@pytest.mark.django_db
def test_registration_post_creates_user(client):
    data = {
        "username": "charlie",
        "first_name": "Charlie",
        "last_name": "C",
        "password1": "XyZ12345!xyZ",
        "password2": "XyZ12345!xyZ",
    }
    r = client.post(reverse("create", current_app="users"), data=data)
    assert r.status_code in (302, 301)
    assert User.objects.filter(username="charlie").exists()


@pytest.mark.django_db
def test_update_requires_auth_redirects(client, users):
    url = reverse("update", args=[users["alice"].pk], current_app="users")
    r = client.get(url)
    assert r.status_code in (302, 301)
    assert reverse("login") in r.url
    assert f"next={url}" in r.url


@pytest.mark.django_db
def test_user_can_update_self(auth_client, users):
    url = reverse("update", args=[users["alice"].pk], current_app="users")
    r_get = auth_client.get(url)
    assert r_get.status_code == 200

    r_post = auth_client.post(
        url,
        data={"username": "alice_new", "first_name": "Al", "last_name": "A"},
    )
    assert r_post.status_code in (302, 301)

    users["alice"].refresh_from_db()
    assert users["alice"].username == "alice_new"
    assert users["alice"].first_name == "Al"


@pytest.mark.django_db
def test_user_cannot_update_other(auth_client, users):
    url = reverse("update", args=[users["bob"].pk], current_app="users")
    r = auth_client.post(url, data={"username": "bob_hacked"})
    assert r.status_code in (302, 403, 404)
    users["bob"].refresh_from_db()
    assert users["bob"].username == "bob"


@pytest.mark.django_db
def test_delete_requires_auth_redirects(client, users):
    url = reverse("delete", args=[users["alice"].pk], current_app="users")
    r = client.get(url)
    assert r.status_code in (302, 301)
    assert reverse("login") in r.url


@pytest.mark.django_db
def test_user_can_delete_self(users):
    c = Client()
    c.login(username="bob", password=users["password"])
    url = reverse("delete", args=[users["bob"].pk], current_app="users")
    r_get = c.get(url)
    assert r_get.status_code == 200
    r_post = c.post(url)
    assert r_post.status_code in (302, 301)
    assert not User.objects.filter(pk=users["bob"].pk).exists()


@pytest.mark.django_db
def test_user_cannot_delete_other(auth_client, users):
    url = reverse("delete", args=[users["bob"].pk], current_app="users")
    r = auth_client.post(url)
    assert r.status_code in (302, 403, 404)
    assert User.objects.filter(pk=users["bob"].pk).exists()


@pytest.mark.django_db
def test_only_author_can_delete(auth_client, users, status_new):
    t = Task.objects.create(
        name="Чужая задача",
        description="...",
        status=status_new,
        author=users["bob"],
    )
    r = auth_client.post(reverse("tasks:delete", args=[t.pk]))
    assert r.status_code in (302, 301)
    assert Task.objects.filter(pk=t.pk).exists()

    c = Client()
    c.login(username="bob", password=users["password"])
    r2 = c.post(reverse("tasks:delete", args=[t.pk]))
    assert r2.status_code in (302, 301)
    assert not Task.objects.filter(pk=t.pk).exists()


@pytest.mark.django_db
def test_user_with_tasks_cannot_be_deleted(users, status_new):
    Task.objects.create(
        name="Тестовая",
        description="Проверка",
        status=status_new,
        author=users["bob"],
    )

    c = Client()
    c.login(username="bob", password=users["password"])
    url = reverse("delete", args=[users["bob"].pk], current_app="users")
    r = c.post(url)
    assert r.status_code in (302, 301)
    assert User.objects.filter(pk=users["bob"].pk).exists()
