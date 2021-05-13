from django.db import models
from user.models import User
from PIL import Image
# Create your models here.

class Advisor(models.Model):
    name = models.CharField(max_length=50)
    profile_pic=models.URLField(max_length=200)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking')
    time = models.DateTimeField()
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
