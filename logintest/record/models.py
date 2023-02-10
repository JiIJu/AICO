from django.db import models
from django.conf import settings

# Create your models here.
class Record(models.Model):
    exercise = models.CharField(max_length=50)
    count = models.IntegerField()
    time = models.IntegerField()
    date = models.DateField(auto_now_add=False)
    perfect = models.IntegerField()
    good = models.IntegerField()
    bad = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

class Image(models.Model):
    image_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
 
    def __str__(self):
        return self.image_name