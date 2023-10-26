from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FileSerializer
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from .models import File
from .tasks import RouterTask
from rest_framework.request import Request


class UploadApiView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        file = self.serializer_class(data=request.data)

        if file.is_valid():
            file.save()
            RouterTask(file).delay()
            return Response(
                file.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            file.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class FilesApiView(APIView):
    def get(self, request: Request) -> Response:
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)
