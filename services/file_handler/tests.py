import tempfile
import os
import time

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, TestCase
from .models import File
from .serializers import FileSerializer
from datetime import datetime
from.tasks import txt, image, pdf, docx, unexpected


class InfoTest(APITestCase):
    url = reverse("info")

    def test_methods(self):
        response = self.client.post(self.url)
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(self.url)
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_good_request(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), {"upload/": "POST", "files/": "GET"})


class UploadTest(APITestCase):
    url = reverse("update")
    test_dir = tempfile.mkdtemp()

    def test_methods(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(self.url)
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_empty_body(self):
        response = self.client.post(self.url)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.json(), {'file': ['No file was submitted.']})

    @override_settings(MEDIA_ROOT=test_dir)
    def test_good_request(self):
        file = SimpleUploadedFile("test_file.txt", b"test,test")
        response = self.client.post(self.url, {"file": file})

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(os.path.isfile(self.test_dir + "/test_file.txt"))

        self.assertEquals(response.json()["file"], "/test_file.txt")

        self.assertEquals(response.json(), FileSerializer(File.objects.get(file="test_file.txt")).data)

    @override_settings(MEDIA_ROOT=test_dir)
    def test_long_name(self):
        file = SimpleUploadedFile(f"{str([i for i in range(100)])}.txt", b"test,test")
        response = self.client.post(self.url, {"file": file})

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.json(), {'file': ['Ensure this filename has at most 100 characters (it has 255).']})


class FilesApiView(APITestCase):
    url = reverse("files")

    def setUp(self):
        File.objects.create(file="test.txt", upload_at=datetime.now(), processed=False)
        File.objects.create(file="test2.txt", upload_at=datetime.now(), processed=False)

    def test_method(self):
        response = self.client.post(self.url)
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(self.url)
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_good_request(self):
        response = self.client.get(self.url).json()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response), 2)

        self.assertEquals(response[1].get("file"), "/test2.txt")


class CeleryTest(TestCase):

    def setUp(self):
        File.objects.create(file="test.txt", upload_at=datetime.now(), processed=False)
        File.objects.create(file="test.pdf", upload_at=datetime.now(), processed=False)
        File.objects.create(file="test.docx", upload_at=datetime.now(), processed=False)
        File.objects.create(file="test.jpg", upload_at=datetime.now(), processed=False)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_task(self):
        result = txt.delay(1)
        time.sleep(6)
        self.assertTrue(result.successful())

        result = image.delay(1)
        time.sleep(6)
        self.assertTrue(result.successful())

        result = pdf.delay(1)
        time.sleep(6)
        self.assertTrue(result.successful())

        result = docx.delay(1)
        time.sleep(6)
        self.assertTrue(result.successful())

        result = unexpected.delay(1)
        time.sleep(6)
        self.assertTrue(result.successful())
