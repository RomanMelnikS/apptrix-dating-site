import django_filters as filters
from geopy.distance import great_circle

from .models import CustomUser


class ClientsFilter(filters.FilterSet):
    """Фильтр списка участников(пользователей).

    Fields:
        sex (char): Фильтрация списка по полу участника.
        first_name (char): Фильтрация списка по имени участника.
        last_name (char): Фильтрация списка по фамилии участника.
        location (int): Фильтрация списка по дистанции между участниками.
    """
    location = filters.NumberFilter(
        method='get_location'
    )

    def get_location(self, queryset, name, value):
        """Определение дистанции между участниками.
        """
        client = self.request.user

        if client.is_authenticated and client.location is not None:
            client_position = (
                client.location.latitude,
                client.location.longitude
            )
            positions = [client.id]
            for user in queryset:
                user_position = (
                    user.location.latitude,
                    user.location.longitude
                )
                distance = great_circle(client_position, user_position).km
                if value < distance:
                    positions.append(user.id)
            return queryset.exclude(id__in=positions)
        return queryset

    class Meta:
        model = CustomUser
        fields = (
            'sex',
            'first_name',
            'last_name',
            'location'
        )
