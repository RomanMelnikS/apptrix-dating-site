from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import ClientsFilter
from .models import CustomUser, Match
from .serializers import ClientsSerializer, MatchesSerializer


class ClientCreateView(CreateAPIView):
    """Регистрация(создание) нового пользователя(участника).
    """
    queryset = CustomUser.objects.all()
    serializer_class = ClientsSerializer


class ClientsView(ListAPIView):
    """Представление списка всех пользователей(участников).
    """
    queryset = CustomUser.objects.all()
    serializer_class = ClientsSerializer
    filterset_class = ClientsFilter


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def match(request, id=None):
    """Создание симпатий между пользователями(участниками).

    Если симпатии взаимны происходит отправка уведомлений на электронную почту
    кождого участника.

    Args:
        id (int, optional): id понравившегося участника. По умолчанию None.

    Vars:
        liking_client (CustomUser) : Участник, создающий симпатию.
        liked_client (CustomUser) : Участник, которому оставили симпатию.

    """
    liking_client = request.user
    liked_client = get_object_or_404(
        CustomUser,
        id=id
    )
    if request.method == 'POST':
        serializer = MatchesSerializer(
            data={
                'liking_client': liking_client.id,
                'liked_client': liked_client.id
            },
            context={
                'request': request
            }
        )
        if serializer.is_valid():
            serializer.save()
            if Match.objects.filter(
                liking_client=liked_client.id
            ).exists():
                clients = [liking_client, liked_client]
                head = 'Взаимная симпатия!'
                for client in clients:
                    body = f'Вы понравились {client.first_name}!' \
                        f'\nПочта участника: {client.email}'
                    send_mail(
                        head,
                        body,
                        None,
                        [client.email]
                    )
                return Response(
                    {
                        'Взаимная симпатия с клиентом, вот его Email':
                            liked_client.email
                    }
                )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
