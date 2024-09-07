from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password')
    def create(self, clean_data):
        user_obj = UserModel.objects.create_user(
            username=clean_data['username'], 
            password=clean_data['password']
        )
        user_obj.email = clean_data['email']
        user_obj.save()
        return user_obj

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        user = authenticate(
            username=clean_data['username'], 
            password=clean_data['password']
        )
        if user:
            return user
        else:
            raise serializers.ValidationError('Usuario no encontrado')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'email')
