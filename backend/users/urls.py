from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import ClientCreateView, ClientsView, match


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_summary='Создание токена.',
        tags=['Аутенфикация']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_summary='Обновление токена.',
        tags=['Аутенфикация']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


urlpatterns = [
    path(
        'clients/create/',
        ClientCreateView.as_view(),
        name='client_create'
    ),
    path(
        'clients/<int:id>/match/',
        match,
        name='match'
    ),
    path(
        'clients/token/login/',
        DecoratedTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'clients/token/refresh/',
        DecoratedTokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'list/',
        ClientsView.as_view(),
        name='clients_list'
    ),
]
