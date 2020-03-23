from django.shortcuts import render
from .models import Chat
from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from chatting.models import message
from .forms import messageForm
from operator import attrgetter
from itertools import chain
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

def msg_view(request, var):
	m1 = User.objects.get(pk = var)
	m2 = User.objects.get(username = request.user)
	obj1 = message.objects.filter(sender = m2, receiver = m1)
	obj2 = message.objects.filter(receiver = m2, sender = m1)
	result_list = sorted(chain(obj1, obj2),key=attrgetter('timestamp'))
	if request.method == 'POST':
		form = messageForm(request.POST)
		if form.is_valid():
			f = form.save(commit = False)
			# f.sender = m2 
			# f.receiver = m1
			new_msg = message.objects.create(sender = m2, receiver = m1, text = f.text)
			# f.save()
			return redirect('msg_view', var = m1.pk)

#things in data base can also be saved by eliminating line 46 and uncommenting line 44, 45, 47, 


	for msg in result_list:
		print(type(msg.sender.username),'   ',type(m1.username),'   ',type(msg.receiver.username))

	else:
		form = messageForm()
		
	return render(request, 'chatting/msg_view.html', {'conversation':result_list, 'form':form, 'A':request.user.username, 'B':m1.username})

# def msg_view_api(request):
# 	if request.method == 'POST':
# 		y = json.loads(request.body)
# 		sender = y['sender']
# 		receiver = y['receiver']
# 		text = y['text']
# 		esend = y['esend']
# 		erec = y['erec']
# 		obj0 = message.objects.filter(sender.email = esend)
# 		obj3 = message.objects.filter(receiver.email = erec)
# 		obj1 = message.sender =(sender)
# 		obj2 = message.receiver =(receiver)
# 		message.objects.create(sender = obj0, receiver = obj3, text = text)
# 		data = {
# 			'message' : 'sucessfull'
# 		}
# 		return JsonRepsonse(data, safe = False)
# 	else:
# 		data = {
# 			'message' : 'unsucessfull'
# 		}
# 		return JsonRepsonse(data, safe = False)

def msg_list(request):
	sent_list = []
	received_list = []
	sent = message.objects.filter(sender = request.user)
	received = message.objects.filter(receiver = request.user)
	for x in sent:
		if x.receiver.username not in sent_list:
			sent_list.append(x.receiver)

	for y in received:
		if y.sender.username not in received_list:
			received_list.append(y.sender)

	print(received_list,'    ', sent_list)

	final_list = list(set(received_list) | set(sent_list)) 

	print(request.path_info)

	return render(request, 'chatting/msg_list.html', {'msgs':final_list})








