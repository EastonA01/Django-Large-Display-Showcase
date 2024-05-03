from django import forms
from hello.models import LogMessage, ChatMessage

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message",)   # NOTE: the trailing comma is required

class BlogMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ("message",)   # NOTE: the trailing comma is required