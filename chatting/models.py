from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
# Create your models here.
class Chat(models.Model):
	user_from = models.CharField(max_length = 100)
	user_to = models.CharField(max_length = 100)
	date = models.DateTimeField(blank = True, null = True, default=timezone.now())
	msg = models.TextField()

	def publish(self):
		self.date = timezone.now()
		self.save()

	def __str__(self):
		return self.user_from


class message(models.Model):
	text = models.TextField(max_length=120)
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank = True, related_name = "sender")
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank = True, related_name = "receiver")
	timestamp = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.sender)+' to '+str(self.receiver)
