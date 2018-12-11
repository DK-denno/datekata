from .models import Profile,Messages
from django import forms



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        fields = ['dp','bio']

class MessagForm(forms.ModelForm):
    class Meta:
        model = Messages
        exclude = []
        fields = ['message']