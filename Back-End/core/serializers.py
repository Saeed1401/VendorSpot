from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer, 
    UserSerializer as BaseUserSerializer,
)
from rest_framework import serializers



class UserCreateSerializer(BaseUserCreateSerializer):
    confirm_password = serializers.CharField(
        write_only=True, 
        style={
            "input_type": "password",
            "placeholder": "confirm your password",
        }
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Passwords do not match!!')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        return super().create(validated_data)
    
 
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'id', 
            'username', 
            'password', 
            'confirm_password',
            'email', 
            'first_name', 
            'last_name', 
            'language', 
            'gender'
        ]


        

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            'id', 
            'username', 
            'password', 
            'email', 
            'first_name', 
            'last_name', 
            'language', 
            'gender'
        ]