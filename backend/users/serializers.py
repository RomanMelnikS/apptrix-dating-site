from rest_framework import serializers

from .models import CustomUser


class ClientsSerializer(serializers.ModelSerializer):
    sex = serializers.ChoiceField(choices=['м', 'ж'])
    avatar = serializers.ImageField()

    class Meta:
        fields = (
            'email',
            'password',
            'username',
            'first_name',
            'last_name',
            'sex',
            'avatar'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }
        model = CustomUser

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
