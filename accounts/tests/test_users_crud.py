from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UsersCrudBasicTests(TestCase):
    def setUp(self):
        self.password = "P@ssw0rd12345"
        self.user1 = User.objects.create_user(
            username="alice", password=self.password,
            first_name="Alice", last_name="A"
        )
        self.user2 = User.objects.create_user(
            username="bob", password=self.password,
            first_name="Bob", last_name="B"
        )

    # ---- LIST (public) ----
    def test_users_list_is_public(self):
        resp = self.client.get(reverse("users:list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "alice")
        self.assertContains(resp, "bob")

    # ---- CREATE (registration) ----
    def test_registration_get(self):
        resp = self.client.get(reverse("users:create"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'name="username"')
        self.assertContains(resp, 'name="password1"')
        self.assertContains(resp, 'name="password2"')

    def test_registration_post_creates_user(self):
        payload = {
            "username": "charlie",
            "first_name": "Charlie",
            "last_name": "C",
            "password1": "XyZ12345!xyZ",
            "password2": "XyZ12345!xyZ",
        }
        resp = self.client.post(reverse("users:create"), data=payload)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username="charlie").exists())

    # ---- UPDATE (only self) ----
    def test_update_requires_auth_redirects(self):
        url = reverse("users:update", args=[self.user1.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_user_can_update_self(self):
        self.client.login(username="alice", password=self.password)
        url = reverse("users:update", args=[self.user1.pk])
        resp_get = self.client.get(url)
        self.assertEqual(resp_get.status_code, 200)

        payload = {"username": "alice_new", "first_name": "Al", "last_name": "A"}
        resp_post = self.client.post(url, data=payload)
        self.assertEqual(resp_post.status_code, 302)

        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, "alice_new")
        self.assertEqual(self.user1.first_name, "Al")

    def test_user_cannot_update_other(self):
        self.client.login(username="alice", password=self.password)
        url = reverse("users:update", args=[self.user2.pk])
        resp = self.client.post(url, data={"username": "bob_hacked"})
        self.assertIn(resp.status_code, (302, 403, 404))
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.username, "bob")

    # ---- DELETE (only self) ----
    def test_delete_requires_auth_redirects(self):
        url = reverse("users:delete", args=[self.user1.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_user_can_delete_self(self):
        self.client.login(username="bob", password=self.password)
        url = reverse("users:delete", args=[self.user2.pk])
        resp_get = self.client.get(url)
        self.assertEqual(resp_get.status_code, 200)
        resp_post = self.client.post(url)
        self.assertEqual(resp_post.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user2.pk).exists())

    def test_user_cannot_delete_other(self):
        self.client.login(username="alice", password=self.password)
        url = reverse("users:delete", args=[self.user2.pk])
        resp = self.client.post(url)
        self.assertIn(resp.status_code, (302, 403, 404))
        self.assertTrue(User.objects.filter(pk=self.user2.pk).exists())
