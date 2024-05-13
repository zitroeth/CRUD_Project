from rest_framework import viewsets
from . import models
from . import serializers
from transformers import pipeline
from rest_framework.response import Response
from rest_framework import status

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
class SentimentAnalysisViewSet(viewsets.ModelViewSet):
    queryset = models.SentimentAnalysis.objects.all()
    serializer_class = serializers.SentimentAnalysisSerializer

    def create(self, request):
        text = request.data.get('text')
        if not text:
            return Response({'error': 'Missing text field in request data'}, status=status.HTTP_400_BAD_REQUEST)

        sentiment_result = sentiment_model([text])[0]
        print(sentiment_result)
        sentiment = 'Positive' if sentiment_result['label'] == 'LABEL_1' else 'Negative'

        sentiment_analysis = models.SentimentAnalysis(text=text, sentiment=sentiment, score=sentiment_result['score'])
        sentiment_analysis.save()

        return Response({'text': text, 'sentiment': sentiment, 'score': sentiment_result['score']}, status=status.HTTP_201_CREATED)