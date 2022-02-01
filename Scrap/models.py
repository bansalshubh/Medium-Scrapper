from django.db import models

# Create your models here.

class SearchHistory(models.Model):
    SearchId = models.AutoField(primary_key=True)
    SearchTagName = models.CharField(max_length=500)
    SearchDate = models.DateField()