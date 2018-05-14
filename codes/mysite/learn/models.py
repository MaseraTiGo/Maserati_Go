from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=30)
    sex = models.CharField(max_length=8)
    age = models.IntegerField()
    def __str__(self):
        return self.name