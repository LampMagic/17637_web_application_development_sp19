from django.shortcuts import render

from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from socialnetwork.forms import LoginForm, RegistrationForm, CreateForm, \
                                EditForm, PostForm, CommentForm, ProfileForm

@login_required
def global_stream_action(request):
    context = {}

    if request.method == 'GET':
        context['postform'] = PostForm()
        context['commentform_1'] = CommentForm()
        context['commentform_2'] = CommentForm()
        return render(request, 'socialnetwork/global_stream.html', context)

    return redirect(reverse('global_stream'))

@login_required
def follower_stream_action(request):
    context = {}

    if request.method == 'GET':
        context['postform'] = PostForm()
        context['commentform_1'] = CommentForm()
        context['commentform_2'] = CommentForm()
        return render(request, 'socialnetwork/follower_stream.html', context)

    return redirect(reverse('follower_stream'))

@login_required
def follower_action(request):
    context = {}

    if request.method == 'GET':
        context['postform'] = ProfileForm()
        return render(request, 'socialnetwork/follower.html', context)

    return redirect(reverse('follower'))

@login_required
def profile_action(request):
    context = {}

    if request.method == 'GET':
        context['postform'] = ProfileForm()
        return render(request, 'socialnetwork/profile.html', context)

    return redirect(reverse('profile'))

@login_required
def create_action(request):
    if request.method == 'GET':
        context = { 'form': CreateForm() }
        return render(request, 'socialnetwork/create.html', context)

    create_form = CreateForm(request.POST)
    if not create_form.is_valid():
        context = { 'form': create_form }
        return render(request, 'socialnetwork/create.html', context)

    dummy_entry = { 'id': 1 }
    for field in [ 'last_name', 'first_name', 'birthday',
                'address', 'city', 'state', 'zip_code', 'country',
                'email', 'home_phone', 'cell_phone', 'fax',
                'spouse_last', 'spouse_first', 'spouse_birth', 'spouse_cell', 'spouse_email' ]:
        dummy_entry[field] = create_form.cleaned_data[field]

    dummy_entry['created_by']    = request.user
    dummy_entry['creation_time'] = timezone.now()
    dummy_entry['updated_by']    = request.user
    dummy_entry['update_time']  = timezone.now()

    message = 'Entry created'
    edit_form = EditForm(dummy_entry)
    context = { 'message': message, 'entry': dummy_entry, 'form': edit_form }
    return render(request, 'socialnetwork/edit.html', context)

@login_required
def delete_action(request, id):
    if request.method != 'POST':
        message = 'Invalid request.  POST method must be used.'
        return render(request, 'socialnetwork/search.html', { 'message': message })

    entry = lookup_entry(id)
    if entry == None:
        context = { 'message': 'Record with id={0} does not exist'.format(id) }
        return render(request, 'socialnetwork/search.html', context)

    message = 'Entry for {0}, {1} has been deleted ... NOT!'.format(entry['last_name'], entry['first_name'])
    return render(request, 'socialnetwork/search.html', { 'message': message })

@login_required
def edit_action(request, id):
    if request.method == 'GET':
        entry = lookup_entry(id)
        if entry == None:
            context = { 'message': 'Record with id={0} does not exist'.format(id) }
            return render(request, 'socialnetwork/search.html', context)

        # Fill in dummy time and user data
        entry['created_by']    = request.user
        entry['creation_time'] = timezone.now()
        entry['updated_by']    = request.user
        entry['update_time']  = timezone.now()

        form = EditForm(entry)
        context = { 'entry': entry, 'form': form }
        return render(request, 'socialnetwork/edit.html', context)


    edit_form = EditForm(request.POST)
    if not edit_form.is_valid():
        # Fill in dummy time and user data
        entry = {'id': id }
        entry['created_by']    = request.user
        entry['creation_time'] = timezone.now()
        entry['updated_by']    = request.user
        entry['update_time']  = timezone.now()

        context = { 'form': edit_form, 'entry': entry }
        return render(request, 'socialnetwork/edit.html', context)

    entry = { 'id': id }
    for field in [ 'last_name', 'first_name', 'birthday',
                'address', 'city', 'state', 'zip_code', 'country',
                'email', 'home_phone', 'cell_phone', 'fax',
                'spouse_last', 'spouse_first', 'spouse_birth', 'spouse_cell', 'spouse_email' ]:
        entry[field] = edit_form.cleaned_data[field]

    entry['created_by']    = request.user
    entry['creation_time'] = timezone.now()
    entry['updated_by']    = request.user
    entry['update_time']  = timezone.now()

    message = 'Entry Updated'
    context = { 'message': message, 'entry': entry, 'form': edit_form }
    return render(request, 'socialnetwork/edit.html', context)

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

    login(request, new_user)
    return redirect(reverse('home'))


def lookup_entry(id):
    if (id == 41):
        return BUSH_41_ENTRY
    if (id == 43):
        return BUSH_43_ENTRY
    if (id == 45):
        return TRUMP_ENTRY
    return None


TRUMP_ENTRY = {
    'id': 45,
    'last_name':    'Trump',
    'first_name':   'Donald',
    'address':      '1600 Pennsylvania Avenue',
    'city':         'Washington',
    'state':        'DC',
    'spouse_last':  'Trump',
    'spouse_first': 'Melania',
}

BUSH_41_ENTRY = {
    'id': 41,
    'last_name':    'Bush',
    'first_name':   'George',
    'spouse_last':  'Bush',
    'spouse_first': 'Barbara',
}

BUSH_43_ENTRY = {
    'id': 43,
    'last_name':    'Bush',
    'first_name':   'George',
    'spouse_last':  'Bush',
    'spouse_first': 'Laura',
}
