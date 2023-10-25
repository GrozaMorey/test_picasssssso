from django.urls import path
from .views import UploadApiView, FilesApiView


urlpatterns = [
    path("files/", FilesApiView.as_view()),
    path("upload/", UploadApiView.as_view())
]
