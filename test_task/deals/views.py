import os

from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework import status

from deals.models import User
from deals.serializers import TopFiveSerializer
from deals.utils import read_csv_data
from test_task.settings import MEDIA_ROOT


class DealMixin(CreateModelMixin,
                ListModelMixin,
                GenericViewSet):
    pass


class DealViewSet(DealMixin):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TopFiveSerializer

    def create(self, request, *args, **kwargs):
        try:
            file = request.FILES['deals']
        except MultiValueDictKeyError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'Status': 'Error',
                    'Desc': 'No file was atteched'
                }
            )
        fs = FileSystemStorage()
        if file.name.split('.')[-1] != 'csv':
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'Status': 'Error',
                    'Desc': 'Only .csv files available'
                }
            )
        filename = fs.save(file.name, file)
        result = read_csv_data(os.path.join(MEDIA_ROOT, filename))
        if result:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'Status': 'Error', 'Desc': result}
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data={'Status': 'OK'}
        )

    def list(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(self.queryset, many=True)

        return Response(serializer.data)