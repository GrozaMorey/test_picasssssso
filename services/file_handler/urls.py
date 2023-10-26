from django.urls import path
from .views import UploadApiView, FilesApiView, Api_info


urlpatterns = [
    path("files/", FilesApiView.as_view(), name="files"),
    path("upload/", UploadApiView.as_view(), name="update"),
    path("", Api_info.as_view(), name="info")
]
