import os

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.conf import settings
from .serializers import ImageSerializer

from . import image_recognition


class ImageRecognitionView(APIView):
    parser_class = (FileUploadParser,)
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        image_serializer = self.serializer_class(data=request.data)

        if image_serializer.is_valid():
            image_serializer.save()
            img_path = image_serializer.data.get('file')
            img_name = '/'.join(img_path.split('/')[2:])
            url = os.path.join(settings.MEDIA_ROOT, img_name)
            images = image_recognition.do_query(url, 5)
            return Response({'images': images}, status=status.HTTP_200_OK)
        else:
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
