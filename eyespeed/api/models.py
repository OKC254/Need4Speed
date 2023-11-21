from django.db import models

# Create your models here.
class VideoUpload(models.Model):
    caption = models.CharField(max_length=40, null=True)
    videofile=models.FileField(upload_to='media/%y')
    speedlimit=models.IntegerField()

    def __str__(self):
        return self.caption