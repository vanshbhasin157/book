from django import forms
from .models import Books
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 

class BookForm(forms.ModelForm):
	
	class Meta:
		model = Books
		fields = ['book_name', 'book_img']

class UserRegisterForm(UserCreationForm): 
    email = forms.EmailField() 
    phone_no = forms.CharField(max_length = 20) 
    first_name = forms.CharField(max_length = 20) 
    last_name = forms.CharField(max_length = 20) 
    class Meta: 
        model = User 
        fields = ['username', 'email', 'phone_no', 'password1', 'password2'] 

class EditProfile(UserChangeForm):

	class Meta:
		model = User
		fields = {'first_name', 'last_name', 'email'}