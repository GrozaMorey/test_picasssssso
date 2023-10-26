from celery import shared_task
import time
from .models import File
from .serializers import FileSerializer


@shared_task
def image(file_id: int):
    file = File.objects.get(id=file_id)
    time.sleep(5)
    file.processed = True
    file.save()


@shared_task
def docx(file_id: int):
    file = File.objects.get(id=file_id)
    time.sleep(5)
    file.processed = True
    file.save()


@shared_task
def pdf(file_id: int):
    file = File.objects.get(id=file_id)
    time.sleep(5)
    file.processed = True
    file.save()


@shared_task
def txt(file_id: int):
    file = File.objects.get(id=file_id)
    time.sleep(5)
    file.processed = True
    file.save()


@shared_task
def unexpected(file_id: int):
    file = File.objects.get(id=file_id)
    time.sleep(5)
    file.processed = True
    file.save()


class RouterTask:
    extension = str
    file_id = int
    routers = {
        "png": image,
        "jpeg": image,
        "jpg": image,
        "docx": docx,
        "pdf": pdf,
        "txt": txt,
    }

    def __init__(self, file: FileSerializer):
        self.extension = file.data.get("file").split(".")[-1].lower()
        self.file_id = file.data.get("id")

    def delay(self):
        if self.extension in self.routers:
            self.routers[self.extension].delay(self.file_id)
        else:
            unexpected.delay(self.file_id)
