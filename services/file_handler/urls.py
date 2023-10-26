from django.urls import path
from .views import UploadApiView, FilesApiView, InfoApi


urlpatterns = [
    path("files/", FilesApiView.as_view(), name="files"),
    path("upload/", UploadApiView.as_view(), name="update"),
    path("", InfoApi.as_view(), name="info")
]
