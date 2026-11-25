from rest_framework import viewsets
from .serializers import ExpeditionSerializer
from .models import Expedition

class ExpeditionViewSet(viewsets.ModelViewSet):
  queryset = Expedition.objects.all()
  serializer_class = ExpeditionSerializer