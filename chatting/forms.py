from django import forms
from .models import message


class messageForm(forms.ModelForm):
	
	class Meta:
		model = message
		fields = ('text',)