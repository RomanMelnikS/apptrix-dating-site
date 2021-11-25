from django.urls import path

from .views import ClientCreate

urlpatterns = [
    path('clients/create/', ClientCreate.as_view()),
]
