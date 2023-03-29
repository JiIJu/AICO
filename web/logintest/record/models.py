from django.db import models
from django.conf import settings

# Create your models here.
class Record(models.Model):
    exercise = models.CharField(max_length=50)
    count = models.IntegerField()
    time = models.IntegerField()
    date = models.DateField(auto_now_add=False)
    good = models.IntegerField()
    bad = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

