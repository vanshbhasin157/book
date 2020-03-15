from django.shortcuts import render
from .models import Chat
from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
# Create your views here.

def baatein(request):
	if request.method == 'POST':
		y = json.loads(request.body)
		sender = y['sender']
		receiver = y['receiver']
		msg = y['msg']
		datetime = timezone.now()
		Chat.objects.create(user_from = sender, user_to = receiver, msg = msg)
		return HttpResponse('suces')




