from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Users, Skill
from django.core import mail


class AuthAndUserFlowTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.user_data_url = reverse("user-data")
        self.skill_list_url = reverse("skill-list-create")

    def test_register_login_and_get_user_data(self):
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "test@example.com",
            "phone": "+1234567890",
            "password": "strongpass123",
            "confirm_password": "strongpass123",
            "address": "123 Street",
        }
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Users.objects.filter(username="testuser").exists())
        # OTP email should be sent
        self.assertGreaterEqual(len(mail.outbox), 1)

        user = Users.objects.get(username="testuser")
        user.is_active = True
        user.save()

        login_response = self.client.post(
            self.login_url,
            {"username": "testuser", "password": "strongpass123"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_202_ACCEPTED)
        access = login_response.data.get("access")
        self.assertIsNotNone(access)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        data_response = self.client.get(self.user_data_url)
        self.assertEqual(data_response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_response.data["data"]["username"], "testuser")

    def test_add_and_list_skills(self):
        user = Users.objects.create_user(
            username="skilluser",
            email="skill@example.com",
            password="strongpass123",
            address="123 Street",
        )
        user.is_active = True
        user.save()

        login_response = self.client.post(
            self.login_url,
            {"username": "skilluser", "password": "strongpass123"},
            format="json",
        )
        access = login_response.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        create_resp = self.client.post(
            self.skill_list_url, {"skill_name": "Python"}, format="json"
        )
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Skill.objects.filter(user=user, skill_name="Python").exists()
        )

        list_resp = self.client.get(self.skill_list_url)
        self.assertEqual(list_resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(list_resp.data["skills"]), 1)

