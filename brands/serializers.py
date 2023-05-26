from rest_framework import serializers
from .models import CarBrand, CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):  # Добавление доп. полей в токен
        token = super().get_token(user)
        token['custom_field'] = user.custom_field
        return token

    def validate(self, attrs):  # Валидация токена
        data = super().validate(attrs)
        return data


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = '__all__'

    def validate_country(self, value):
        # Пример валидации поля "country"
        valid_countries = ["South Korea", "Germany", "Japan", 'France']

        if value not in valid_countries:
            raise serializers.ValidationError("Недопустимая страна производства.")
        return value

    def validate_name(self, value):
        # valid_name = ['BMW X5', 'Toyota Camry', 'Hyundai Sonata', 'Citroen C5']
        names = CarBrand.objects.all()
        for i in names:
            if value.lower() == i.name.lower():
                raise serializers.ValidationError("Такая тачка уже записана")
        # if value not in valid_name:
        #   raise serializers.ValidationError("Недопустимая названия.")
        return value

    def validate_info(self, value):
        valid = 'абвгдеёжзийклмнопрстуфхцчшщьъыэюя'
        for i in value.lower():
            if i in valid:
                raise serializers.ValidationError("Русские буквы нельзя.")
        else:
            return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'is_editor']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_editor': {'read_only': True}}

    def create(self, validated_data):
        validated_data['is_editor'] = True
        user = CustomUser.objects.create_user(**validated_data)
        return user
