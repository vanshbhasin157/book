from django.db import models

# Create your models here.

class Books(models.Model):
	book_name = models.CharField(max_length = 150)
	book_img = models.ImageField(upload_to='images/') 
	author = models.CharField(max_length = 150, null =True)

	def __str__(self):
		return self.book_name
