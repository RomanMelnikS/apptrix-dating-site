from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import CustomUser, Match


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
        avatar = self.validated_data.pop('avatar')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.avatar.save(user.username + '_avatar.jpg', add_watermark(avatar))
        user.save()
        return user


class MatchesSerializer(serializers.ModelSerializer):

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
    img = Image.open(avatar).convert('RGBA').resize((1200, 960))
    watermark = Image.open('backend_static/watermark.png').convert('RGBA')
    watermark.thumbnail((1000, 500), Image.ANTIALIAS)
    img.paste(watermark, (700, 450), mask=watermark)
    buffer = BytesIO()
    img.convert('RGB').save(buffer, 'png')
    content = ContentFile(buffer.getvalue())
    buffer.close()
    return content
