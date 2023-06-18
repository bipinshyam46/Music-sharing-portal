from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    class Meta:
        db_table='Usertable'

class Musiclist(models.Model):
    title=models.TextField(verbose_name='Song title')
    artist = models.TextField(verbose_name='Artist')
    audio_file = models.FileField(upload_to='music/')
    status=models.TextField(default='public')
    access=models.EmailField(blank=True,max_length=1000)

class Regemails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @staticmethod
    def get_registered_emails():
        return Regemails.objects.values_list('email', flat=True)