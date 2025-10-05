# tests/test_statuses_simple.py
import pytest
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.test import Client

from statuses.models import Status
from tasks.models import Task


@pytest.fixture
def user(db):
    return User.objects.create_user(username="u", password="p12345678")


@pytest.fixture
def auth_client(user):
    c = Client()
    c.login(username="u", password="p12345678")
    return c


@pytest.mark.django_db
def test_login_required(client):
    r1 = client.get("/statuses/")
    r2 = client.get("/statuses/create/")
    assert r1.status_code in (302, 301)
    assert r2.status_code in (302, 301)
    assert "login" in r1.url
    assert "login" in r2.url


@pytest.mark.django_db
def test_list(auth_client):
    Status.objects.create(name="новый")
    Status.objects.create(name="в работе")
    resp = auth_client.get("/statuses/")
    assert resp.status_code == 200
    html = resp.content.decode()
    assert "новый" in html
    assert "в работе" in html


@pytest.mark.django_db
def test_create(auth_client):
    resp = auth_client.post("/statuses/create/", data={"name": "на тестировании"})
    assert resp.status_code in (302, 301)
    assert Status.objects.filter(name="на тестировании").exists()


@pytest.mark.django_db
def test_update(auth_client):
    st = Status.objects.create(name="черновик")
    resp = auth_client.post(f"/statuses/{st.pk}/update/", data={"name": "завершён"})
    assert resp.status_code in (302, 301)
    st.refresh_from_db()
    assert st.name == "завершён"


@pytest.mark.django_db
def test_delete(auth_client):
    st = Status.objects.create(name="временный")
    get_resp = auth_client.get(f"/statuses/{st.pk}/delete/")
    assert get_resp.status_code == 200
    post_resp = auth_client.post(f"/statuses/{st.pk}/delete/")
    assert post_resp.status_code in (302, 301)
    assert not Status.objects.filter(pk=st.pk).exists()


@pytest.mark.django_db
def test_cannot_delete_status_in_use(django_user_model):
    user = django_user_model.objects.create_user(username="alice", password="p123")
    status = Status.objects.create(name="новый")
    Task.objects.create(
        name="Тестовая задача",
        description="Проверка связи",
        status=status,
        author=user,
    )

    with pytest.raises(ProtectedError):
        status.delete()
