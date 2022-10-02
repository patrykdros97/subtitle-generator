from dataclasses import fields
from django import forms
from .models import UploadMediaFile

class UploadMediaFileForm(forms.Form):
    class Meta:
        model = UploadMediaFile
        fields = {
            'title',
            'file'
        }