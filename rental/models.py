from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Friend(models.Model):
    name = models.CharField(max_length=100)
class Belonging(models.Model):
    name = models.CharField(max_length=100)
class Borrowed(models.Model):
    what = models.ForeignKey(Belonging, on_delete=models.CASCADE)
    to_who = models.ForeignKey(Friend, on_delete=models.CASCADE)
    when = models.DateTimeField(auto_now_add=True)
    returned = models.DateTimeField(null=True, blank=True)
class SentimentAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    sentiment = models.CharField(max_length=10, null=True, editable=False)
    score = models.DecimalField(max_digits=4, decimal_places=3, editable=False, default=0.000)