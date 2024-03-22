from rest_framework import serializers

from users.models import CustomUser
PHONE_REGEX = r'^\+?1?\d{9,15}$'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.RegexField(regex=PHONE_REGEX,
                                   error_messages={'invalid': 'El número de teléfono no es válido'})
    hobbies = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'hobbies','password')
    def create(self, validated_data):
        return CustomUser(**validated_data)
