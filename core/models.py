from django.db import models

# Create your models here.
class UploadMediaFile(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)