import django_filters as filters
from geopy.distance import great_circle

from .models import CustomUser


class ClientsFilter(filters.FilterSet):
    location = filters.NumberFilter(
        method='get_location'
    )

    def get_location(self, queryset, name, value):
        if self.request.user.is_authenticated:
            client = self.request.user
            client_position = (
                client.location.latitude,
                client.location.longitude
            )
            positions = [client.id]
            if client.location is not None:
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
