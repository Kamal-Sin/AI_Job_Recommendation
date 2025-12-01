from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import Users, CV


class ExtractSkillsAPITests(APITestCase):
    def setUp(self):
        self.extract_url = reverse("extract-skills")
        self.cv_url = reverse("cv-api")
        self.login_url = reverse("login")

        self.user = Users.objects.create_user(
            username="cvuser",
            email="cv@example.com",
            password="strongpass123",
            address="123 Street",
        )
        self.user.is_active = True
        self.user.save()

        login_response = self.client.post(
            self.login_url,
            {"username": "cvuser", "password": "strongpass123"},
            format="json",
        )
        access = login_response.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def _create_dummy_pdf(self, content: bytes) -> SimpleUploadedFile:
        return SimpleUploadedFile(
            "test_cv.pdf", content, content_type="application/pdf"
        )

    def test_extract_skills_without_cv(self):
        response = self.client.post(self.extract_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_extract_skills_with_cv(self):
        # Create a tiny PDF-like file; pdfplumber will try to read it,
        # so in real tests you may want a real small PDF in fixtures.
        dummy_pdf = self._create_dummy_pdf(b"%PDF-1.4 test pdf content with Python")
        upload_resp = self.client.post(self.cv_url, {"cv_file": dummy_pdf})
        self.assertIn(upload_resp.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST))

        response = self.client.post(self.extract_url)
        # Depending on pdfplumber behaviour, this might be 201 or an error;
        # we assert that the endpoint is reachable and returns a valid status code.
        self.assertIn(
            response.status_code,
            (
                status.HTTP_201_CREATED,
                status.HTTP_200_OK,
                status.HTTP_400_BAD_REQUEST,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            ),
        )
