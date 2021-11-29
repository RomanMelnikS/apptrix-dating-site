from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import ClientCreateView, ClientsView, match

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
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'clients/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'list/',
        ClientsView.as_view(),
        name='clients_list'
    ),
]
