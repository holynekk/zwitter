from django.conf import settings
from django import forms
from .models import Tweet

MAX_ZWEET_LENGTH = settings.MAX_ZWEET_LENGTH

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_ZWEET_LENGTH:
            raise forms.ValidationError("The tweet is too long")
        return content