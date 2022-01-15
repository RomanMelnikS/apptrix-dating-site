from io import BytesIO

from django.core.files.base import ContentFile
from drf_extra_fields.fields import Base64ImageField
from PIL import Image
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import CustomUser, Location, Match


class LocationSerializer(serializers.ModelSerializer):
    """Сериализация модели локации участника(пользователя).
    """
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

    class Meta:
        fields = (
            'longitude',
            'latitude'
        )
        model = Location


class ClientsSerializer(serializers.ModelSerializer):
    """Сериализация модели участника(пользователя).
    """
    sex = serializers.ChoiceField(choices=['м', 'ж'])
    avatar = Base64ImageField()
    location = LocationSerializer()

    class Meta:
        fields = (
            'email',
            'password',
            'username',
            'first_name',
            'last_name',
            'sex',
            'avatar',
            'location'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }
        model = CustomUser

    def create(self, validated_data):
        loc = validated_data.pop('location')
        avatar = validated_data.pop('avatar')
        location = Location.objects.create(**loc)
        user = CustomUser.objects.create(location=location, **validated_data)
        location.client = user
        location.save()
        user.avatar.save(
            user.username + '_avatar.jpg', add_watermark(avatar)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MatchesSerializer(serializers.ModelSerializer):
    """Сериализация модели симпатий участников.
    """

    class Meta:
        fields = ('__all__')
        model = Match
        validators = [
            UniqueTogetherValidator(
                queryset=Match.objects.all(),
                fields=['liking_client', 'liked_client']
            )
        ]

    def validate(self, data):
        if self.context['request'].user != data.get('liked_client'):
            return data
        raise serializers.ValidationError(
            'Нельзя понравится самому себе!'
        )

    def to_representation(self, instance):
        serializer = ClientsSerializer(
            instance.liked_client,
            context=self.context
        )
        return serializer.data


def add_watermark(avatar):
    """Добавление водяного знака на аватар участника.

    Args:
        avatar (img): Аватар участника без водяного знака.

    Vars:
        img (Image): Подготовленный для обработка аватар.
        watermark (Image): Водяной знак.

    Returns:
        content (ContentFile): Обработанный аватар с водяным знаком.
    """
    img = Image.open(avatar).convert('RGBA').resize((1200, 960))
    watermark = Image.open('watermark.png').convert('RGBA')
    watermark.thumbnail((1000, 500), Image.ANTIALIAS)
    img.paste(watermark, (700, 450), mask=watermark)
    buffer = BytesIO()
    img.convert('RGB').save(buffer, 'png')
    content = ContentFile(buffer.getvalue())
    buffer.close()
    return content
