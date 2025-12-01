from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Users, Skill


class JobRecommendationAPITests(APITestCase):
    def setUp(self):
        self.recommendations_url = reverse("job-recommendations")
        self.login_url = reverse("login")
        self.user = Users.objects.create_user(
            username="jobuser",
            email="job@example.com",
            password="strongpass123",
            address="123 Street",
        )
        self.user.is_active = True
        self.user.save()
        Skill.objects.create(user=self.user, skill_name="Python")

        login_response = self.client.post(
            self.login_url,
            {"username": "jobuser", "password": "strongpass123"},
            format="json",
        )
        self.access = login_response.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

    def test_get_recommendations(self):
        response = self.client.get(self.recommendations_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("recommendations", response.data)
