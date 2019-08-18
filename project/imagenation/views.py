from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone, dateparse
from django.urls import path
from django.utils.dateparse import parse_datetime
from django.core.files import File 
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import urllib

from imagenation.forms import *
from imagenation.models import *

MAX_UPLOAD_SIZE = 5000000

def free_upload_action(request):
	if request.method == 'GET':
		context = {'form': PhotoForm()}
		return render(request, 'imagenation/free_upload.html', context)

	upload_photo = Photo()
	upload_photo.time = timezone.now()

	if request.method != 'POST':
		message = 'Upload photo using POST request'
		context = {'message': message, 'form': PhotoForm()}
		return render(request, 'imagenation/free_upload.html', context)

	if not request.FILES:
		message = 'No photo selected'
		context = {'message': message, 'form': PhotoForm()}
		return render(request, 'imagenation/free_upload.html', context)

	create_form = PhotoForm(request.POST, request.FILES, instance=upload_photo)
	if not create_form.is_valid():
		message = 'Invalid photo'
		context = {'message': message, 'form': PhotoForm()}
		return render(request, 'imagenation/free_upload.html', context)
	else:
		pic = create_form.cleaned_data['photo']
		if not pic.content_type or not pic.content_type.startswith('image'):
			message = 'Invalid photo'
			context = {'message': message, 'form': PhotoForm()}
			return render(request, 'imagenation/free_upload.html', context)
		if pic.size > MAX_UPLOAD_SIZE:
			message = 'File too large'
			context = {'message': message, 'form': PhotoForm()}
			return render(request, 'imagenation/free_upload.html', context)

		upload_photo.dtype = pic.content_type
		create_form.save()
		message = 'Photo uploaded'
		context = {'message': message, 'photo': upload_photo, 'form': PhotoForm()}
		return redirect(reverse('free_edit', args=[upload_photo.id]))

@login_required
def upload_action(request):
	if request.method == 'GET':
		context = {'form': PhotoForm(), 'user': request.user}
		return render(request, 'imagenation/upload.html', context)

	upload_photo = Photo()
	upload_photo.owner = request.user
	upload_photo.time = timezone.now()

	if request.method != 'POST':
		message = 'Upload photo using POST request'
		context = {'message': message, 'form': PhotoForm(), 'user': request.user}
		return render(request, 'imagenation/upload.html', context)

	if not request.FILES:
		message = 'No photo selected'
		context = {'message': message, 'form': PhotoForm(), 'user': request.user}
		return render(request, 'imagenation/upload.html', context)

	create_form = PhotoForm(request.POST, request.FILES, instance=upload_photo)
	if not create_form.is_valid():
		message = 'Invalid photo'
		context = {'message': message, 'form': PhotoForm(), 'user': request.user}
		return render(request, 'imagenation/upload.html', context)
	else:
		pic = create_form.cleaned_data['photo']
		if not pic.content_type or not pic.content_type.startswith('image'):
			message = 'Invalid photo'
			context = {'message': message, 'form': PhotoForm(), 'user': request.user}
			return render(request, 'imagenation/upload.html', context)
		if pic.size > MAX_UPLOAD_SIZE:
			message = 'File too large'
			context = {'message': message, 'form': PhotoForm(), 'user': request.user}
			return render(request, 'imagenation/upload.html', context)

		upload_photo.dtype = pic.content_type
		create_form.save()
		message = 'Photo uploaded'
		context = {'message': message, 'photo': upload_photo,
				   'form': PhotoForm(),'user': request.user}
		return redirect(reverse('edit_photo', args=[upload_photo.id]))

def free_edit_action(request, id):
	prev_photo = get_object_or_404(Photo, id=id)

	if request.method == 'GET':
		context = {'photo': prev_photo, 'form': PhotoForm()}
		return render(request, 'imagenation/free_edit.html', context)

	upload_photo = Photo()
	upload_photo.time = timezone.now()

	if request.method != 'POST':
		message = 'Upload photo using POST request'
		context = {'message': message, 'form': PhotoForm()}
		return render(request, 'imagenation/free_edit.html', context)

	if not request.FILES:
		context = {'photo': prev_photo, 'form': PhotoForm()}
		return render(request, 'imagenation/free_edit.html', context)

	create_form = PhotoForm(request.POST, request.FILES, instance=upload_photo)
	if not create_form.is_valid():
		message = 'Invalid photo'
		context = {'message': message, 'photo': prev_photo, 'form': PhotoForm()}
		return render(request, 'imagenation/free_edit.html', context)
	else:
		pic = create_form.cleaned_data['photo']
		if not pic.content_type or not pic.content_type.startswith('image'):
			message = 'Invalid photo'
			context = {'message': message, 'form': PhotoForm()}
			return render(request, 'imagenation/free_edit.html', context)
		if pic.size > MAX_UPLOAD_SIZE:
			message = 'File too large'
			context = {'message': message, 'form': PhotoForm()}
			return render(request, 'imagenation/free_edit.html', context)

		upload_photo.dtype = pic.content_type
		create_form.save()
		message = 'Photo uploaded'
		context = {'message': message, 'photo': upload_photo, 'form': PhotoForm()}
		return render(request, 'imagenation/free_edit.html', context)

@login_required
def edit_action(request, id):
	prev_photo = get_object_or_404(Photo, id=id)

	if request.method == 'GET':
		tags = prev_photo.tags.all()
		context = {'photo': prev_photo, 'form': PhotoForm(), 'user': request.user, 'tags': tags}
		return render(request, 'imagenation/edit.html', context)

	upload_photo = Photo()
	upload_photo.owner = request.user
	upload_photo.time = timezone.now()

	if request.method != 'POST':
		tags = prev_photo.tags.all()
		message = 'Upload photo using POST request'
		context = {'message': message, 'form': PhotoForm(), 'user': request.user, 'tags': tags}
		return render(request, 'imagenation/edit.html', context)

	if 'tag_input' in request.POST:
		tag_value = request.POST['tag_input'].lower()
		tag_value = tag_value.replace(" ","")
		if tag_value == "":
			print("invalid tag")
		else:
			if Tag.objects.filter(tag=tag_value).count()==0:
				tag = Tag(tag=tag_value)
				tag.count+=1
				tag.save()
			else:
				tag = Tag.objects.get(tag=tag_value)
				tag.count+=1
				tag.save()
			
			prev_photo.tags.add(tag)
			prev_photo.save()

	if not request.FILES:
		tags = prev_photo.tags.all()
		context = { 'photo': prev_photo,
				   'form': PhotoForm(), 'user': request.user, 'tags': tags}
		return render(request, 'imagenation/edit.html', context)

	create_form = PhotoForm(request.POST, request.FILES, instance=upload_photo)
	if not create_form.is_valid():
		message = 'Invalid photo'
		context = {'message': message, 'photo': prev_photo,
				   'form': PhotoForm(), 'user': request.user, 'tags': prev_photo.tags.all()}
		return render(request, 'imagenation/edit.html', context)
	else:
		pic = create_form.cleaned_data['photo']
		if not pic.content_type or not pic.content_type.startswith('image'):
			message = 'Invalid photo'
			context = {'message': message, 'form': PhotoForm(), 'user': request.user,'tags': prev_photo.tags.all()}
			return render(request, 'imagenation/edit.html', context)
		if pic.size > MAX_UPLOAD_SIZE:
			message = 'File too large'
			context = {'message': message, 'form': PhotoForm(), 'user': request.user,'tags': prev_photo.tags.all()}
			return render(request, 'imagenation/edit.html', context)

		upload_photo.dtype = pic.content_type
		create_form.save()
		message = 'Photo uploaded'
		context = {'message': message, 'photo': upload_photo,
			   'form': PhotoForm(),'user': request.user}
		return render(request, 'imagenation/edit.html', context)

# @login_required
def get_photo(request, id):
	photo = get_object_or_404(Photo, id=id)
	# Maybe we don't need this check as form validation requires a picture be uploaded.
	# But someone could have delete the picture leaving the DB with a bad references.
	# if not photo.upload:
	# 	raise Http404
	# print(HttpResponse(photo.photo, content_type=photo.dtype))
	return HttpResponse(photo.photo, content_type=photo.dtype)

@login_required
def send_email(request, id):
	prev_photo = get_object_or_404(Photo, id=id)

	tags = prev_photo.tags.all()

	subject = "Your ImageNation Photo"
	body_text = "Hi " + request.user.username + ",\n Here is the photo you requested.\nThe ImageNation Team\n"
	message = EmailMultiAlternatives(
	    subject=subject,
	    body=body_text,
	    from_email=settings.EMAIL_HOST_USER,
	    to=[request.user.email,],
	)
	message.attach_file(prev_photo.photo.path)
	message.send(fail_silently=False)

	context = {'photo': prev_photo, 'form': PhotoForm(), 'user': request.user, 'tags': tags}
	return render(request, 'imagenation/edit.html', context)

@login_required
def save_photo(request, id):
	cur_photo = get_object_or_404(Photo, id=id)

	if request.method != 'POST':
		message = "Save photo using POST request"
		context = {'message': message, 'photo': cur_photo,
				   'form': PhotoForm(),'user': request.user}
		return render(request, 'imagenation/edit.html', context)

	if not request.FILES:
		message = "No photo found"
		context = {'message': message, 'photo': cur_photo,
				   'form': PhotoForm(),'user': request.user}
		return render(request, 'imagenation/edit.html', context)

	cur_photo.photo = request.FILES['photo']
	cur_photo.dtype = request.FILES['photo'].content_type
	cur_photo.save()

	message = 'Photo saved'
	context = {'message': message, 'photo': cur_photo,
			   'form': PhotoForm(),'user': request.user}
	return render(request, 'imagenation/edit.html', context)

@login_required
def publish_photo(request, id):
	cur_photo = get_object_or_404(Photo, id=id)

	if cur_photo.share is True:
		cur_photo.share = False
	else:
		cur_photo.share = True
	cur_photo.save()

	photos = Photo.objects.filter(owner=request.user)
	context = {'user': request.user, 'photos': photos}
	return render(request, 'imagenation/profile.html', context)

@login_required
def profile_action(request):
	photos = Photo.objects.filter(owner=request.user)
	context = {'user': request.user, 'photos': photos}
	return render(request, 'imagenation/profile.html', context)

@login_required
def other_user_action(request, id):
	try:
		owner = User.objects.get(id=id)
	except ObjectDoesNotExist:
		raise Http404
	if owner == request.user:
		return profile_action(request)

	photos = Photo.objects.filter(owner=owner, share=True)
	context = {'owner': owner, 'photos': photos}
	return render(request, 'imagenation/other_user.html', context)

@login_required
def society_action(request):
	photos = Photo.objects.filter(share=True)
	tags = Tag.objects.all()
	context = {'user': request.user, 'photos': photos, 'tags':tags}
	return render(request, 'imagenation/society.html', context)

@login_required
def photo_detail(request,id):
	photo = get_object_or_404(Photo, id=id)
	owner = photo.owner
	tags = photo.tags.all()

	try:
		profile = Profile.objects.get(user=request.user)
	except ObjectDoesNotExist:
		raise Http404

	like_photos = profile.like_photos.all()

	like_check = like_photos.filter(id=id)

	like_text = 'Unlike'
	like_status = True
	
	if request.method == 'GET':
		if like_check.count() == 0:
			like_text = 'Like'
			like_status = False	

	else:
		if 'like_btn' not in request.POST or not request.POST['like_btn']:
			message = "Error Button!"
			if like_check.count() == 0:
				like_text = 'Like'
				like_status = False
						
			context = {'user': request.user, 'photo': photo, 'tags':tags, 'owner':owner, 'like_text':like_text }
			return render(request, 'socialnetwork/follower.html', context)

		if like_check.count() == 0:
			like_text = 'Like'
			like_status = False

		if request.POST['like_btn'] == 'click':
			if like_status == True:
				like_text = 'Like'
				like_status = False
				profile.like_photos.remove(photo)
				profile.save()
				photo.likes-=1;
				photo.save()
			else:
				like_text = 'Unike'
				like_status = True
				profile.like_photos.add(photo)
				profile.save()
				photo.likes+=1;
				photo.save()

	context = {'user': request.user, 'photo': photo, 'tags':tags, 'owner':owner, 'like_text':like_text }
	return render(request, 'imagenation/photo_detail.html', context)

@login_required
def tag_action(request,id):
	try:
		tag_object = Tag.objects.get(id=id)
	except ObjectDoesNotExist:
		raise Http404
	
	photos = Photo.objects.filter(share=True,tags__in=[tag_object])|Photo.objects.filter(owner=request.user,tags__in=[tag_object])
	tags = Tag.objects.filter(count__gt=0)
	context = {'user': request.user, 'photos': photos, 'tags':tags,'tag_object':tag_object}
	return render(request, 'imagenation/tag_page.html', context)

@login_required
def delete_photo(request, id):
	try:
		photo = Photo.objects.get(id=id)
		for tag in photo.tags.all():
			tag.count -= 1
			if tag.count == 0:
				tag.delete()
		photo.delete()
	except ObjectDoesNotExist:
		photos = Photo.objects.filter(owner=request.user)
		message = "Invalid photo id"
		context = {'user': request.user, 'photos': photos, 'message': message}
		return render(request, 'imagenation/profile.html', context)

	photos = Photo.objects.filter(owner=request.user)
	message = "Delete successfully"
	context = {'user': request.user, 'photos': photos, 'message': message}
	return render(request, 'imagenation/profile.html', context)

def login_action(request):
	context = {}

	# Just display the registration form if this is a GET request.
	if request.method == 'GET':
		context['form'] = LoginForm()
		return render(request, 'imagenation/login.html', context)

	# Creates a bound form from the request POST parameters and makes the 
	# form available in the request context dictionary.
	form = LoginForm(request.POST)
	context['form'] = form

	# Validates the form.
	if not form.is_valid():
		return render(request, 'imagenation/login.html', context)

	new_user = authenticate(username=form.cleaned_data['username'],
	                        password=form.cleaned_data['password'])

	login(request, new_user)
	return redirect(reverse('home'))

def logout_action(request):
	logout(request)
	return redirect(reverse('login'))

def register_action(request):
	context = {}

	# Just display the registration form if this is a GET request.
	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'imagenation/register.html', context)

	# Creates a bound form from the request POST parameters and makes the 
	# form available in the request context dictionary.
	form = RegistrationForm(request.POST)
	context['form'] = form

    # Validates the form.
	if not form.is_valid():
		return render(request, 'imagenation/register.html', context)

	# At this point, the form data is valid.  Register and login the user.
	new_user = User.objects.create_user(username=form.cleaned_data['username'], 
	                                password=form.cleaned_data['password1'],
	                                email=form.cleaned_data['email'],
	                                first_name=form.cleaned_data['first_name'],
	                                last_name=form.cleaned_data['last_name'])
	new_user.save()
	new_user = authenticate(username=form.cleaned_data['username'],
	                        password=form.cleaned_data['password1'])

	login(request, new_user)
	profile = Profile.objects.filter(user = request.user)

	if profile.count() == 0:
		profile = Profile(user = request.user)
		profile.save()

	return redirect(reverse('home'))
