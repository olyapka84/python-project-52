import pytest
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.tasks.models import Task, Status


@pytest.mark.django_db
def test_labels_list_requires_login(client):
    url = reverse("labels:index")
    resp = client.get(url)
    assert resp.status_code == 302
    assert reverse("users:login") in resp["Location"]


@pytest.mark.django_db
def test_label_create_requires_login(client):
    url = reverse("labels:create")
    resp = client.post(url, {"name": "bug"})
    assert resp.status_code == 302
    assert reverse("users:login") in resp["Location"]
    assert not Label.objects.filter(name="bug").exists()


@pytest.mark.django_db
def test_label_create_ok(client, django_user_model):
    django_user_model.objects.create_user(username="u", password="p")
    client.login(username="u", password="p")

    url = reverse("labels:create")
    resp = client.post(url, {"name": "bug"})
    assert resp.status_code == 302
    obj = Label.objects.get(name="bug")
    assert obj.name == "bug"


@pytest.mark.django_db
def test_label_update_ok(client, django_user_model):
    django_user_model.objects.create_user(username="u", password="p")
    client.login(username="u", password="p")

    label = Label.objects.create(name="old")
    url = reverse("labels:update", args=[label.pk])
    resp = client.post(url, {"name": "new"})
    assert resp.status_code == 302

    label.refresh_from_db()
    assert label.name == "new"


@pytest.mark.django_db
def test_label_delete_blocked_when_in_use(client, django_user_model):
    user = django_user_model.objects.create_user(username="u", password="p")
    client.login(username="u", password="p")

    label = Label.objects.create(name="bug")
    status = Status.objects.create(name="open")
    task = Task.objects.create(name="t1", author=user, status=status)
    task.labels.add(label)

    url = reverse("labels:delete", args=[label.pk])
    resp_get = client.get(url)
    assert resp_get.status_code in (200, 302)

    resp_post = client.post(url)
    assert resp_post.status_code == 302
    assert Label.objects.filter(pk=label.pk).exists()


@pytest.mark.django_db
def test_label_delete_when_unused_ok(client, django_user_model):
    django_user_model.objects.create_user(username="u", password="p")
    client.login(username="u", password="p")

    label = Label.objects.create(name="orphan")
    url = reverse("labels:delete", args=[label.pk])
    resp = client.post(url)
    assert resp.status_code == 302
    assert not Label.objects.filter(pk=label.pk).exists()
