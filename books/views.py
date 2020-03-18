from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm, EditProfile
from .models import Books
from django.db.models import Q
from django.contrib import messages 
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import AuthenticationForm 
from .forms import UserRegisterForm 
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import json

# Create your views here.
@login_required 
def book_view(request): 

	if request.method == 'POST': 
		form = BookForm(request.POST, request.FILES) 

		if form.is_valid(): 
			form.save() 
			return redirect('success') 
	else: 
		form = BookForm() 
	return render(request, 'books/upload.html', {'form' : form}) 

@login_required
def success(request): 
	return HttpResponse('successfully uploaded') 


def display(request): 

	if request.method == 'GET': 
 
		Book = Books.objects.all()
		return render(request, 'books/display.html', {'book_images' : Book}) 

def display_api(request):
	if request.method == 'GET':
		y = json.loads(request.body)
		y = Books.objects.all()
		for i in y:

def search(request):
	if request.method == 'POST':
		srh = request.POST['srch']
		if srh:
			match = Books.objects.filter(Q(book_name__icontains=srh))
			if match:
				return render(request,'books/search.html', {'sr':match})
			else:
				return HttpResponse('not found')
		else:
			return HttpResponseRedirect("/search")
	return render(request, 'books/search.html')

def details(request, pk):
	obj1 = get_object_or_404(Books, pk = pk)
	return render(request, 'books/details.html', {'book': obj1})

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_date.get('username')
			email = form.cleaned_date.get('email')
			messages.success(request, f'Your account has been created ! You are now able to log in')
			return redirect('login')
	else:
		form = UserRegisterForm()
		return render(request, 'books/register.html', {'form': form, 'title':'reqister here'})

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
			if user is not None:
				form = login(request, user)
				messages.success(request, f' wecome {username} !!')
				return redirect('display')
			else:
				messages.info(request,f'account done not exit plz sign in')
	form = AuthenticationForm()
	return render(request,'books/login.html', {'form':form, 'title':'log in'})


@login_required
def profile(request):
	return render(request, 'books/profile.html', {})


@login_required
def edit(request):
	if request.method == 'POST':
		form = EditProfile(request.POST, instance = request.user)
		if form.is_valid():
			user = form.save()
			return redirect('profile')
		else:
			messages.error(request, 'Please correct the following errors.')
	else:
		form = EditProfile(instance = request.user)
	return render(request, 'books/profile_edit.html', {'form': form})

@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
			if form.is_valid():
				user = form.save()
				update_session_auth_hash(request,user)
				messages.success(request, 'Your password was successfully updated!')
				return redirect('profile')
			else:
				messages.error(request, 'Please correct the error below.')
	else:
		from = PasswordChangeForm(request.user)
		response = render(request,'books/pass_change.html',{'from':form})
		response.set_cookie('password_changed','true')
		return response

