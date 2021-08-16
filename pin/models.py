from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
	slug = models.SlugField(max_length=100, primary_key=True)
	title = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.title


class Pin(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pins')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='pins')
	title = models.CharField(max_length=100)
	text = models.TextField()
	image = models.ImageField(upload_to='pins', blank=True, null=True)
	link = models.CharField(max_length=200)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
	pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='comments')
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.author


class Rating(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
	pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='ratings')
	rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

	def __str__(self):
		return f'{self.author}: {self.pin} - {self.rating}'
