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
from django.http import JsonResponse
import base64
import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
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

def book_view_api(request):
	if request.method == 'POST':
		y = json.loads(request.body)
		name = y["name"]
		image = base64.b64decode(y['image'])
		imgFromData = Image.open(BytesIO(image))
		ref = "media/images/"+name+".jpg"
		imgFromData.save(ref, quality = 60)
		obj = Books.objects.create(book_name = name, book_img = imgFromData)
		print("ok2")
		data = {
			"message" : "successfull"
		}
		return JsonResponse(data, safe = False)
	else:
		data = {
			"message" : "unsuccessfull"
		}
		return JsonResponse(data, safe = False)

@login_required
def success(request): 
	return HttpResponse('successfully uploaded') 


def display(request): 
	if request.method == 'GET': 
		Book = Books.objects.all()
		return render(request, 'books/display.html', {'book_images' : Book}) 
def display_api(request):
	if request.method == 'GET':
		y = Books.objects.all()
		l = []
		data = {}
		for x in y:
			foo = {}
			foo["name"] = x.book_name
			foo["image"] = x.book_img.url
			l.append(foo)
		data["key"] = l
		return JsonResponse(data, safe = False)
	else:
		data = {
			"message" : "unsuccessfull"
		}
		return JsonResponse(data, safe = False)


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

def search_api(request):
	if request.method == 'POST':
		y = json.loads(request.body)
		l = []
		data = {}
		query = y["query"]
		match =  Books.objects.filter(Q(book_name__icontains= query))
		if match:
			for x in match:
				foo = {}
				foo["name"] = x.book_name
				foo["image"] = x.book_img.url
				l.append(foo)
			data["key"] = l
			return JsonResponse(data, safe = False)
		else:
			data = {
				"message" : "not found"
			}
			return JsonResponse(data, safe = False)




def details(request, pk):
	obj1 = get_object_or_404(Books, pk = pk)
	return render(request, 'books/details.html', {'book': obj1})

def detail_api(request):
	if request.method == 'POST':
		y = json.loads(request.body)
		book_id = y["id"]
		obj = Books.objects.get(pk = book_id)
		data = {
			"title" : obj.book_name,
			"image" : obj.book_img.url
		}
		return JsonResponse(data, safe = False)
	else:
		data = {
			"message" : "Incorrect details"
		}
		return JsonResponse(data, safe = False)

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

def Login(request):
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

def login_api(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		username = data.get('username', None)
		password = data.get('password', None)
		per_user = authenticate(username=username, password=password)
		if per_user is not None:
			response_validity = {"message" : "successful"}
		else:
			response_validity = {"message": "Incorrect details"}
		return JsonResponse(response_validity, safe=False)


@login_required
def profile(request):
	return render(request, 'books/profile.html', {})

def profile_api(request):
	if request.method == 'GET':
		data = {
			"username" : request.user.username,
			"name" : request.user.get_full_name(),
			"email" : request.user.email
		}
		y = json.dumps(data)
		return HttpResponse(JsonResponse(y, safe = False))
	else:
		data = {
				"message" : "Not logged in"
			}
		return HttpResponse(JsonResponse(data, safe = False))



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
		form = PasswordChangeForm(request.user)
		response = render(request,'books/pass_change.html',{'from':form})
		response.set_cookie('password_changed','true')
		return response

