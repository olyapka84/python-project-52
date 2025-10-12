from django.db.models import ProtectedError
from django.test import Client

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
pytestmark = pytest.mark.django_db

User = get_user_model()


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
    r1 = client.get(reverse("statuses:index"))
    r2 = client.get(reverse("statuses:create"))
    assert r1.status_code in (302, 301)
    assert r2.status_code in (302, 301)
    assert "login" in r1.url
    assert "login" in r2.url


@pytest.mark.django_db
def test_list(auth_client):
    Status.objects.create(name="новый")
    Status.objects.create(name="в работе")
    resp = auth_client.get(reverse("statuses:index"))
    assert resp.status_code == 200
    html = resp.content.decode()
    assert "новый" in html
    assert "в работе" in html


@pytest.mark.django_db
def test_create(auth_client):
    resp = auth_client.post(reverse("statuses:create"),
                            data={"name": "на тестировании"})
    assert resp.status_code in (302, 301)
    assert Status.objects.filter(name="на тестировании").exists()


@pytest.mark.django_db
def test_update(auth_client):
    st = Status.objects.create(name="черновик")
    resp = auth_client.post(reverse("statuses:update", args=[st.pk]),
                            data={"name": "завершён"})
    assert resp.status_code in (302, 301)
    st.refresh_from_db()
    assert st.name == "завершён"


@pytest.mark.django_db
def test_delete(auth_client):
    st = Status.objects.create(name="временный")
    get_resp = auth_client.get(reverse("statuses:delete", args=[st.pk]))
    assert get_resp.status_code == 200
    post_resp = auth_client.post(reverse("statuses:delete", args=[st.pk]))
    assert post_resp.status_code in (302, 301)
    assert not Status.objects.filter(pk=st.pk).exists()


@pytest.mark.django_db
def test_cannot_delete_status_in_use(django_user_model):
    user = (django_user_model.objects.
            create_user(username="alice", password="p123"))
    status = Status.objects.create(name="новый")
    Task.objects.create(
        name="Тестовая задача",
        description="Проверка связи",
        status=status,
        author=user,
    )

    with pytest.raises(ProtectedError):
        status.delete()