import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status

User = get_user_model()


@pytest.fixture
def status_new(db):
    return Status.objects.create(name="new")


@pytest.fixture
def users(db):
    password = "user-pass-for-tests"
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
    resp = client.get(reverse("users:list"))
    assert resp.status_code == 200
    html = resp.content.decode()
    assert "alice" in html
    assert "bob" in html


@pytest.mark.django_db
def test_registration_get(client):
    r = client.get(reverse("users:create"))
    assert r.status_code == 200
    html = r.content.decode()
    assert 'name="username"' in html
    assert 'name="password1"' in html
    assert 'name="password2"' in html


@pytest.mark.django_db
def test_registration_form_english_texts(client):
    response = client.get(reverse("users:create"))
    assert response.status_code == 200

    html = response.content.decode()
    assert "First name" in html
    assert "Last name" in html
    assert "Password confirmation" in html


@pytest.mark.django_db
def test_login_page_uses_custom_authentication_form(client):
    response = client.get(reverse("login"))
    assert response.status_code == 200

    html = response.content.decode()
    assert "Log in" in html
    assert "Username" in html
    assert "Password" in html


@pytest.mark.django_db
def test_logout_view_logs_user_out(auth_client):
    response = auth_client.post(reverse("logout"))
    assert response.status_code in (302, 301)

    # The logout view should end the session, so following requests must be anonymous
    follow_up = auth_client.get(reverse("home"))
    assert follow_up.wsgi_request.user.is_anonymous


@pytest.mark.django_db
def test_registration_post_creates_user(client):
    data = {
        "username": "charlie",
        "first_name": "Charlie",
        "last_name": "C",
        "password1": "test-pass-123!",
        "password2": "test-pass-123!",
    }
    r = client.post(reverse("users:create"), data=data)
    assert r.status_code in (302, 301)
    assert User.objects.filter(username="charlie").exists()


@pytest.mark.django_db
def test_update_requires_auth_redirects(client, users):
    url = reverse("users:update", args=[users["alice"].pk])
    r = client.get(url)
    assert r.status_code in (302, 301)
    assert reverse("login") in r.url
    assert f"next={url}" in r.url


@pytest.mark.django_db
def test_user_can_update_self(auth_client, users):
    url = reverse("users:update", args=[users["alice"].pk])
    r_get = auth_client.get(url)
    assert r_get.status_code == 200
    html = r_get.content.decode()
    assert "Password" in html
    assert "Password confirmation" in html
    assert "Please enter the password again for confirmation." in html

    r_post = auth_client.post(
        url,
        data={"username": "alice_new", "first_name": "Al", "last_name": "A"},
    )
    assert r_post.status_code in (302, 301)

    users["alice"].refresh_from_db()
    assert users["alice"].username == "alice_new"
    assert users["alice"].first_name == "Al"


@pytest.mark.django_db
def test_user_can_update_password(auth_client, users):
    url = reverse("users:update", args=[users["alice"].pk])
    new_password = "strong-pass-for-tests!1"
    response = auth_client.post(
        url,
        data={
            "username": "alice",
            "first_name": "Alice",
            "last_name": "A",
            "password1": new_password,
            "password2": new_password,
        },
    )

    assert response.status_code in (302, 301)

    users["alice"].refresh_from_db()
    assert users["alice"].check_password(new_password)

    fresh_client = Client()
    assert fresh_client.login(username="alice", password=new_password)


@pytest.mark.django_db
def test_user_update_requires_both_password_fields(auth_client, users):
    url = reverse("users:update", args=[users["alice"].pk])
    response = auth_client.post(
        url,
        data={
            "username": "alice",
            "first_name": "Alice",
            "last_name": "A",
            "password1": "OnlyOnce!",
            "password2": "",
        },
    )

    assert response.status_code == 200
    html = response.content.decode()
    assert "Please enter the password twice." in html


@pytest.mark.django_db
def test_user_update_password_mismatch(auth_client, users):
    url = reverse("users:update", args=[users["alice"].pk])
    response = auth_client.post(
        url,
        data={
            "username": "alice",
            "first_name": "Alice",
            "last_name": "A",
            "password1": "MismatchPass!1",
            "password2": "MismatchPass!2",
        },
    )

    assert response.status_code == 200
    html = response.content.decode()
    assert "The entered passwords do not match." in html


@pytest.mark.django_db
def test_user_cannot_update_other(auth_client, users):
    url = reverse("users:update", args=[users["bob"].pk])
    r = auth_client.post(url, data={"username": "bob_hacked"})
    assert r.status_code in (302, 403, 404)
    users["bob"].refresh_from_db()
    assert users["bob"].username == "bob"


@pytest.mark.django_db
def test_delete_requires_auth_redirects(client, users):
    url = reverse("users:delete", args=[users["alice"].pk])
    r = client.get(url)
    assert r.status_code in (302, 301)
    assert reverse("login") in r.url


@pytest.mark.django_db
def test_user_can_delete_self(users):
    c = Client()
    c.login(username="bob", password=users["password"])
    url = reverse("users:delete", args=[users["bob"].pk])
    r_get = c.get(url)
    assert r_get.status_code == 200
    r_post = c.post(url)
    assert r_post.status_code in (302, 301)
    assert not User.objects.filter(pk=users["bob"].pk).exists()


@pytest.mark.django_db
def test_user_cannot_delete_other(auth_client, users):
    url = reverse("users:delete", args=[users["bob"].pk])
    r = auth_client.post(url)
    assert r.status_code in (302, 403, 404)
    assert User.objects.filter(pk=users["bob"].pk).exists()


@pytest.mark.django_db
def test_only_author_can_delete(auth_client, users, status_new):
    t = Task.objects.create(
        name="Someone else's task",
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
        name="Test",
        description="Check",
        status=status_new,
        author=users["bob"],
    )

    c = Client()
    c.login(username="bob", password=users["password"])
    url = reverse("users:delete", args=[users["bob"].pk])
    r = c.post(url)
    assert r.status_code in (302, 301)
    assert User.objects.filter(pk=users["bob"].pk).exists()
