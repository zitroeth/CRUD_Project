from rest_framework import viewsets
from . import models
from . import serializers
from transformers import pipeline
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from rest_framework import generics
from.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

User = get_user_model()
sentiment_model = pipeline(model="zitroeth/finetuning-distilbert-model-steam-game-reviews")

class FriendViewSet(viewsets.ModelViewSet):
    queryset = models.Friend.objects.all()
    serializer_class = serializers.FriendSerializer
class BelongingViewSet(viewsets.ModelViewSet):
    queryset = models.Belonging.objects.all()
    serializer_class = serializers.BelongingSerializer
class BorrowedViewSet(viewsets.ModelViewSet):
    queryset = models.Borrowed.objects.all()
    serializer_class = serializers.BorrowedSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SentimentAnalysisViewSet(viewsets.ModelViewSet):
    queryset = models.SentimentAnalysis.objects.all()
    serializer_class = serializers.SentimentAnalysisSerializer

    def create(self, request):
        
        text = request.data.get('text')
        if not text:
            return Response({'error': 'Missing text field in request data'}, status=status.HTTP_400_BAD_REQUEST)
        
        # user = request.user
        # print(user)
        sentiment_result = sentiment_model([text])[0]
        print(sentiment_result)
        sentiment = 'Positive' if sentiment_result['label'] == 'LABEL_1' else 'Negative'
       
        sentiment_analysis = models.SentimentAnalysis(text=text, sentiment=sentiment, score=sentiment_result['score'])
        sentiment_analysis.save()

        return Response({'text': text, 'sentiment': sentiment, 'score': sentiment_result['score']}, status=status.HTTP_201_CREATED)
    
    # def destroy(self, request, *args, **kwargs):
        # instance = self.get_object()
        
        # if request.user!= instance.user and not request.user.is_superuser:
        #     return Response({"detail": "You do not have permission to delete this item."}, status=status.HTTP_403_FORBIDDEN)
        
        # self.perform_destroy(instance)
        # return Response(status=status.HTTP_204_NO_CONTENT)