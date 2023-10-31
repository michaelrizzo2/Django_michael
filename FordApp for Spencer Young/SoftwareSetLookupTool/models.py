from django.db import models

# Create your models here.
class BuildUrl(models.Model):
    build_url=models.CharField(max_length=256)