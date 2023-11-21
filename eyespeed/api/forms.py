from django.forms import ModelForm
from .models import VideoUpload
from django import forms

class VideoForm(ModelForm):
    caption = forms.TextInput()
    videofile = forms.FileField()
    speedlimit = forms.IntegerField()
    class Meta:
        model = VideoUpload
        fields = ['caption', 'videofile', 'speedlimit']