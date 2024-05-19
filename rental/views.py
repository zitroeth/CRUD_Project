from rest_framework import viewsets
from . import models
from . import serializers
from transformers import pipeline
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from.serializers import UserSerializer
from django.contrib.auth import get_user_model, authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group


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
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        created_user = serializer.data

        regular_user_group = Group.objects.get(name='RegularUser')


        regular_user_group.user_set.add(created_user['id'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SentimentAnalysisViewSet(viewsets.ModelViewSet):
    queryset = models.SentimentAnalysis.objects.all()
    serializer_class = serializers.SentimentAnalysisSerializer
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

    def create(self, request):
        text = request.data.get('text')    
        
        if not request.user.has_perm('rental.add_sentimentanalysis'):
             raise PermissionDenied()
        
        if not text:
            return Response({'error': 'Missing text field in request data'}, status=status.HTTP_400_BAD_REQUEST)
        
        # user = request.user.username
        # print(f"user is {request}")
        sentiment_result = sentiment_model([text])[0]
        print(sentiment_result)
        sentiment = 'Positive' if sentiment_result['label'] == 'LABEL_1' else 'Negative'
       
        sentiment_analysis = models.SentimentAnalysis(text=text, sentiment=sentiment, score=sentiment_result['score'])
        sentiment_analysis.user = request.user
        sentiment_analysis.save()

        return Response({'user_id': request.user.id, 'text': text, 'sentiment': sentiment, 'score': sentiment_result['score']}, status=status.HTTP_201_CREATED)
         
    def list(self, request):
        
        if not request.user.has_perm('rental.view_sentimentanalysis'):
            raise PermissionDenied()
        
        sentiments = models.SentimentAnalysis.objects.all()
        serializer = self.get_serializer(sentiments, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        try:
            current_user_id = request.user.id
            item = models.SentimentAnalysis.objects.get(pk=pk)
            if item.user_id == current_user_id or request.user.is_superuser:
                item.delete()
                return Response({"message": "Item deleted successfully"}, status=204)
            else:
                return Response({"error": "Unauthorized to delete this item."}, status=status.HTTP_403_FORBIDDEN)
        except models.SentimentAnalysis.DoesNotExist:
            return Response({"error": "Item does not exist"}, status=404)
    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk=None):
        try:
            current_user_id = request.user.id
            user_to_delete = User.objects.get(pk=pk)
            
            if user_to_delete.id == current_user_id or request.user.is_superuser:
                user_to_delete.delete()
                return Response({"message": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Unauthorized to delete this account."}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"error": "Account does not exist"}, status=status.HTTP_404_NOT_FOUND)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Missing username or password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)  # Logs in the user

        # Generate token using Django's Token model
        token, _ = Token.objects.get_or_create(user=user)
        
        print(f'token = {token.key}')
        # Return the token in the response
        return Response({'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)