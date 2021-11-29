import django_filters as filters

from .models import CustomUser


class ClientsFilter(filters.FilterSet):
    location = filters.NumberFilter(
        method='get_location'
    )

    def get_location(self, queryset, name, value):
        if self.request.user.is_authenticated:
            client = self.request.user
            if client.location is not None:
                return queryset.exclude(client__location=None)
            return queryset
        return queryset

    class Meta:
        model = CustomUser
        fields = (
            'sex',
            'first_name',
            'last_name',
            'location'
        )
