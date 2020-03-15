from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.
class Chat(models.Model):
	user_from = models.CharField(max_length = 100)
	user_to = models.CharField(max_length = 100)
	date = models.DateTimeField(default = timezone.now())
	msg = models.TextField()

	def publish(self):
		self.save()

	def __str__(self):
		return self.user_from
