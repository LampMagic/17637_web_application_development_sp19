from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone, dateparse
from django.core import serializers
from django.http import HttpResponse, Http404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from socialnetwork.forms import *
from socialnetwork.models import *

last_refresh = None

@login_required
def add_comment_action(request, id):
    global last_refresh
    if request.method != 'POST':
        raise Http404
    print("in add comment")
    print(last_refresh)

    if not 'newcomment' in request.POST or not request.POST['newcomment']:
        message = 'You must enter text to comment.'
        json_error = '{ "error": "'+message+'" }'
        return HttpResponse(json_error, content_type='application/json')

    new_comment = Comment(user=request.user,
                          first=request.user.first_name,
                          last=request.user.last_name,
                          text=request.POST['newcomment'],
                          time=timezone.now(),
                          post=id)
    new_comment.save()

    response_text = serializers.serialize('json', Comment.objects.filter(post=id, time__gte=last_refresh))
    return HttpResponse(response_text, content_type='application/json')

@login_required
def refresh_global_action(request):
    global last_refresh
    if request.method != 'GET' or not 'last_refresh' in request.GET or not request.GET['last_refresh']:
        raise Http404

    last_refresh = dateparse.parse_datetime(request.GET.get('last_refresh'))
    if last_refresh is None:
        raise Http404

    print("in global")
    print(last_refresh)

    post_text = serializers.serialize('json', Post.objects.filter(time__gte=last_refresh))
    comment_text = serializers.serialize('json', Comment.objects.filter(time__gte=last_refresh))

    if (post_text != '[]') and (comment_text != '[]'):
        response_text = post_text[:-1] + ", " + comment_text[1:]
    elif (post_text != '[]'):
        response_text = post_text
    elif (comment_text != '[]'):
        response_text = comment_text
    else:
        response_text = '[]'
    print(response_text)

    return HttpResponse(response_text, content_type='application/json')

@login_required
def refresh_follower_action(request):
    global last_refresh
    if request.method != 'GET' or not 'last_refresh' in request.GET or not request.GET['last_refresh']:
        raise Http404
    
    last_refresh = dateparse.parse_datetime(request.GET.get('last_refresh'))
    if last_refresh is None:
        raise Http404
        
    print("in follower")
    print(last_refresh)

    request_profile = Profile.objects.get(id=request.user.id)
    post_text = serializers.serialize('json', Post.objects.filter(time__gte=last_refresh,
                                                                  user__in=request_profile.followers.all()).order_by('-time'))
    comment_text = serializers.serialize('json', Comment.objects.filter(time__gte=last_refresh))

    if (post_text != '[]') and (comment_text != '[]'):
        response_text = post_text[:-1] + ", " + comment_text[1:]
    elif (post_text != '[]'):
        response_text = post_text
    elif (comment_text != '[]'):
        response_text = comment_text
    else:
        response_text = '[]'
    print(response_text)

    return HttpResponse(response_text, content_type='application/json')

@login_required
def global_stream_action(request):
    context = {}
    # global stream browsing
    if request.method == 'GET':
        context['posts'] = Post.objects.all().order_by('-time')
        return render(request, 'socialnetwork/global_stream.html', context)
    # global stream posting
    elif request.method == 'POST':
        if 'newpost' not in request.POST or not request.POST['newpost']:
            context['message'] = 'You must enter text to post.'
        else:
            new_post = Post(user=request.user,
                            first=request.user.first_name,
                            last=request.user.last_name,
                            text=request.POST['newpost'],
                            time=timezone.now())
            new_post.save()
    # all other actions
    else:
        context['message'] = 'Add post must be done using the POST method'

    context['posts'] = Post.objects.all().order_by('-time')
    return render(request, 'socialnetwork/global_stream.html', context)

@login_required
def follower_stream_action(request):
    context = {}
    request_profile = Profile.objects.get(id=request.user.id)
    # follower stream browsing
    if request.method == 'GET':
        # posts belonging to followers
        context['posts'] = Post.objects.filter(user__in=request_profile.followers.all()).order_by('-time')
        return render(request, 'socialnetwork/follower_stream.html', context)
    # follower stream posting
    elif request.method == 'POST':
        if 'newcomment' not in request.POST or not request.POST['newcomment']:
            context['message'] = 'You must enter text to post.'
        else:
            new_comment = Post(user=request.user,
                               text=request.POST['newcomment'],
                               time=timezone.now())
            new_comment.save()
    # all other actions
    else:
        context['message'] = 'Add comment must be done using the POST method'

    context['posts'] = Post.objects.filter(user__in=request_profile.followers.all()).order_by('-time')
    return render(request, 'socialnetwork/follower_stream.html', context)

@login_required
def follower_action(request, id):
    context = {}
    # profile page browsing
    if request.method == 'GET':
        # logged in user profile
        if id == request.user.id:
            return profile_action(request)
        # other user profile
        else:
            context['profile'] = Profile.objects.get(id=id)
            request_profile = Profile.objects.get(id=request.user.id)
            # user in followers
            if User.objects.get(id=id) not in request_profile.followers.all():
                context['id_follow'] = 'id_follow'
                context['follow'] = 'Follow'
            # user not in followers
            else:
                context['id_follow'] = 'id_unfollow'
                context['follow'] = 'Unfollow'
            return render(request, 'socialnetwork/follower.html', context)
    # profile page following action
    elif request.method == 'POST':
        if 'follow' not in request.POST or not request.POST['follow']:
            context['message'] = 'You must have follow in POST request.'
        else:
            request_profile = Profile.objects.get(id=request.user.id)
            # toggle follow/unfollow button
            if request.POST['follow'] == 'Follow':
                request_profile.followers.add(User.objects.get(id=id))
                context['id_follow'] = 'id_unfollow'
                context['follow'] = 'Unfollow'
            else:
                request_profile.followers.remove(User.objects.get(id=id))
                context['id_follow'] = 'id_follow'
                context['follow'] = 'Follow'
    # all other actions
    else:
        context['message'] = 'Follow must be done using the POST method'

    context['profile'] = Profile.objects.get(id=id)
    return render(request, 'socialnetwork/follower.html', context)

@login_required
def profile_action(request):
    context = {}
    request_profile = Profile.objects.get(id=request.user.id)
    context['profile'] = request_profile
    context['form'] = ProfileForm()
    # self profile page browsing
    if request.method == 'GET':
        return render(request, 'socialnetwork/profile.html', context)
    # self profile editing
    elif request.method == 'POST':
        request_profile.bio = request.POST.get('bio', request_profile.bio)
        # if image is not uploaded
        if not request.FILES:
            context['form'] = ProfileForm()
        else:
            form = ProfileForm(request.POST, request.FILES, instance=request_profile)
            if not form.is_valid():
                context['form'] = form
            else:
                pic = form.cleaned_data['profile_picture']
                request_profile.content_type = pic.content_type
                form.save()
                context['form'] = ProfileForm()
    # all other actions
    else:
        context['message'] = 'Profile Editing must be done using the POST method'  

    return render(request, 'socialnetwork/profile.html', context)

def get_photo(request, id):
    profile = get_object_or_404(Profile, id=id)
    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not profile.profile_picture:
        raise Http404

    return HttpResponse(profile.profile_picture, content_type=profile.content_type)

def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

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
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])

    new_profile = Profile(user=new_user,
                          bio='Hello, I am '+new_user.first_name+'.')
    new_profile.save()

    login(request, new_user)
    return redirect(reverse('home'))

# test grading script v2