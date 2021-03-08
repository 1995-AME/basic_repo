from django.db import models
import re
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
	def user_validator(self, postData):
		email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		# add keys and values to errors dictionary for each invalid field
		if len(postData['first_name']) < 2 :
			errors['first_name'] = "Your first name must be more than 2 characters."
		if len(postData['last_name']) < 2:
			errors['last_name'] = "Your last name must be more than 2 characters."
		if postData.get('skill_level') == '0':
			errors['skill_level'] = "Please choose a skill level."
		if len(postData.get('desc')) < 5 :
			errors['desc'] = "The description must be more than 5 characters."
		if not email_check.match(postData['email']):
			errors['email'] = "Email must be valid format."
		# has the email already been registered?
		result = User.objects.filter(email=postData['email'])
		if len(result) > 0:
			errors['email'] = "Email address is already registered."
		if len(postData.get('password'))  < 8 :
			errors['password'] = "Password must be at least 8 characters."
		if postData.get('password') != postData.get('confirm_password'):
			errors['confirm_password'] = "Password and confirm password do not match."
		return errors
	def login_validator(self, postData):
		pass



class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	skill_level =models.CharField(max_length=255, default="Beginner")
	desc = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
	# images = posted by the user
	# liked_images = users who like an image
	# messages


# class ImagePostManager(mdoles.Manager)


class UploadImage(models.Model):
	image= models.ImageField(default="default='default.jpg", )
	posted_by = models.ForeignKey(User, related_name="images", on_delete = models.CASCADE)
	likes =  models.ManyToManyField(User, related_name="liked_images")
	title = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


# class MessagePostManager(models.Manager):
# 	def content_validator(self, postData):
# 		errors = {}
# 		if len(postData['content']) < 1 :
# 			errors['title'] = "You must provide content to your post."
# 		return errors

# class MessagePost(models.Model):
# 	content = models.TextField()
# 	subject = models.CharField(max_length=255)
# 	posted_by = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)
# 	objects = MessagePostManager()