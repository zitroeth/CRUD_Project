from rest_framework import serializers
from . import models
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Friend
        fields = ('id', 'name')
class BelongingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Belonging
        fields = ('id', 'name')
class BorrowedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Borrowed
        fields = ('id', 'what', 'to_who', 'when', 'returned')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
class SentimentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SentimentAnalysis
        fields = ('id', 'text', 'sentiment', 'score', 'token')
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Get the user model instance
        user = self.user
        
        # Include the username in the token payload
        data.update({'username': user.username})
        
        return data

class CustomTokenGenerator(RefreshToken):
    @classmethod
    def get_token(cls, user):
        token = cls.for_user(user)
        token_data = token.payload
        token_data['username'] = user.username
        return token