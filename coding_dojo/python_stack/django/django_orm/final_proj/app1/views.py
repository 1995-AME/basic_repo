from django.shortcuts import render, redirect, HttpResponse
from .models import User, UploadImage, UserManager
from django.contrib import messages
import bcrypt
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


# def index(request):
#     return HttpResponse("This is my response!")
#GET Pages
def add_user(request):
	return render(request, 'register.html')

def charities(request):
	return render(request, "charities.html")

#GET Donor Inbox
def donor_mess(request):
	return render(request, 'donor_mess.html')

def gallery(request):
	print("hey, I want to go to the gallery page!")
	context = {
		# 'user' : User.objects.get(id=request.session['user_id']),
		'img' : UploadImage.objects.all()
	}
	return render(request, "gallery.html", context)
	
def index(request):
	print("is this render request even working? ")
	return render(request, "index.html")

def logout(request):
	request.session.flush()
	return redirect('/')

#GET User Inbox
def messages(request):
	return render(request, 'messages.html')

#  GET -  profile page
def profile(request):
	if 'user_id' not in request.session:
		return redirect ('/')
	context = {
		'user' : User.objects.get(id=request.session['user_id']),
	}
	return render(request, "profile.html", context)

#GET Email template
def send_email(request, user_id):
	context = {
		"user" : User.objects.get(id=user_id)
	}
	return render(request, 'email.html', context)

#GET user profile page
def user_profile(request, user_id):
	# if 'user_id' not in request.session:
	# 	return redirect ('/')
	context = {
		'user' : User.objects.get(id=user_id),
	}
	return render(request, "profile.html", context)




# <------POST METHODS------>

#POST - CREATE user
def create_user(request):
	print(" Can I create a user?!")
	if request.method != "POST":
		return redirect('/')
	errors = User.objects.user_validator(request.POST)
		#if the dictionary received has errors in it, reject the form, and show the error messages
		# on the template the user was on last
	if len(errors) > 0:
		print(errors)
		for key, value in errors.items():
			messages.error(request, value)
			return redirect('/')
	else:
		user_pw=request.POST['password']
		# create the hash for the password
		hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
		print(hash_pw)
		# create user object 
		new_user = User.objects.create(
			first_name=request.POST['first_name'], 
			last_name=request.POST['last_name'], 
			email=request.POST['email'], 
			skill_level = request.POST['skill_level'],
			desc = request.POST ['desc'],
			password=hash_pw,
		)
		print(new_user)
		# storing user's id so I can track user's interactions on the website 
		request.session['user_id']= new_user.id 
		request.session['first_name'] = new_user.first_name
		request.session['last_name'] = new_user.last_name
	return redirect('/profile')

#POST - Login Method
def user_login(request):
	print('Is this user_login method working?')
	if request.method == 'POST':
		# query to find the user
		logged_user=User.objects.filter(email=request.POST['email'])

		if len(logged_user) > 0:
			logged_user = logged_user[0]
			print(logged_user)
			print(logged_user.password, request.POST['password'])

			if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
				request.session['user_id'] = logged_user.id 
				request.session['first_name'] = logged_user.first_name
				return redirect ('/profile')
			else :
				messages.error(request, "Your password is incorrect.")
				return redirect ('/')
		else:
			messages.error(request, "Your email does not exist.")
			return redirect ('/')
	return redirect('/profile')

#POST - UPDATE/Edit user information 
def edit(request, user_id):
	print("I MUST edit this form!")
	if request.method == "POST":
		print("is this update working?")
		edit_user = User.objects.get(id=user_id)
		edit_user.desc=request.POST['desc']
		edit_user.save()
	return redirect('/profile')

#POST: upload image to profile page
def upload_image(request):
	UploadImage.objects.create(
		image=request.FILES['image'],
		title=request.FILES['image'].name,
		posted_by=User.objects.get(id=request.session['user_id'])
	)
	return redirect('/profile')

#POST : delete images from profile page
def delete_image(request, image_id):
	if 'user_id' not in request.session:
		return redirect ('/')
	delete_image=UploadImage.objects.get(id=image_id)
	delete_image.delete()
	return redirect ('/profile')

#POSTS - upload imag to gallery 
def upload_image_gallery(request):
	if request.method == "POST":
		UploadImage.objects.create(
			image=request.FILES['image'],
			title=request.FILES['image'].name,
			posted_by=User.objects.get(id=request.session['user_id'])
		)
	return redirect('/gallery')

#POST - Delete from gallery  
def delete_image2(request, image_id):
	if 'user_id' not in request.session:
		return redirect ('/')
	delete_image=UploadImage.objects.get(id=image_id)
	delete_image.delete()
	return redirect ('/gallery')

def contact(request, user_id):
	if request.method == "POST":
		user =User.objects.get(id=user_id)
		subject = request.POST['subject']
		content = request.POST['content']
		email = request.POST['email']
	try:
		#send an email
		send_mail(
			subject, #subject
			content, #content
			'crochetcharity282@gmail.com',
			[user.email],
			fail_silently = False,
		)
		return HttpResponse('Message Sent Successfully!')
	except BadHeaderError:
		return HttpResponse('Invalid header found.')
	# 	return HttpResponseRedirect('/')
	else:
		return HttpResponse('Make sure all fields are entered and valid.')
	return render(request, "/", {'content'})



