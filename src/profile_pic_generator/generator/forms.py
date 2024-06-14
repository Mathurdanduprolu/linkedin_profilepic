from django import forms
from .models import ProfilePicture

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = ProfilePicture
        fields = ['original_image']