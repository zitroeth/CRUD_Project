from rest_framework import serializers
from . import models
from django.contrib.auth.hashers import make_password

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
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
class SentimentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SentimentAnalysis
        fields = ('id', 'user', 'text', 'sentiment', 'score')