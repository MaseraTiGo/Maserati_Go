from django.db import models

# Create your models here.
class Movies(models.Model):
    title = models.CharField(max_length = 150)
    pic = models.ImageField(upload_to = 'media')
    summary = models.CharField(max_length = 500)
    date_old = models.DateField()
    date_new = models.DateField()