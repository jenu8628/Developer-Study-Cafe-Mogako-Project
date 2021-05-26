from django.db import models

# Create your models here.

class Image(models.Model):
    uploaded_image = models.ImageField(upload_to="%Y/%m/%d")
    img_url = models.URLField()