from django.db import models

# Create your models here.

class Tweet(models.Model):
    content = models.TextField(max_length=280, blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)