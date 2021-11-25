from rest_framework.generics import CreateAPIView
from .models import CustomUser
from .serializers import ClientsSerializer


class ClientCreate(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ClientsSerializer
