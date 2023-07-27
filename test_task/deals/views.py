import os
from collections import Counter
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework import status

from deals.models import User
from deals.serializers import TopFiveSerializer
from deals.utils import ReadCSV
from test_task.settings import MEDIA_ROOT


class DealMixin(CreateModelMixin,
                ListModelMixin,
                GenericViewSet):
    pass


class DealViewSet(DealMixin):
    TOP_N = 5
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
                    'Desc': 'No file was attached'
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
        result = ReadCSV(os.path.join(MEDIA_ROOT, filename)).start()
        if result:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'Status': 'Error', 'Desc': result}
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data={'Status': 'OK'}
        )

    def only_popular_gems(self, data):
        all_gems = [gem for item in data for gem in item['gems']]
        counts = Counter(all_gems)
        popular_gems = set([gem for gem in all_gems if counts[gem] > 1])
        for item in data:
            gems = item['gems']
            item['gems'] = [gem for gem in gems if gem in popular_gems]
        return data

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        data = sorted(
            serializer.data,
            key=(lambda x: x['spent_money']),
            reverse=True
        )
        data = data[:self.TOP_N] if len(data) >= self.TOP_N else data
        self.only_popular_gems(data)
        return Response(
            data,
            status=status.HTTP_200_OK
        )
