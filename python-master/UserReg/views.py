from django.shortcuts import render

# Create your views here.
#views.py
from UserReg.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
 
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )

@csrf_protect
@login_required
def update_profile(request):
    message = ""
    if request.method == 'POST':
        user = User.objects.get(username__iexact=request.user)
        if user.check_password(request.POST['oldpass']) and request.POST['newpass'] and request.POST['newpass'] == request.POST['newpassrep']:
            user.set_password(request.POST['newpass'])
            user.save();
            message = "Done Successfully!!"
        else:
            message = "Error Occured!!"
    return render_to_response('update.html',RequestContext(request, {'message':message}))
 
def update_done(request):
    return render_to_response(
    'update_done.html',{}
    )

def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
def home(request):
    return render_to_response(
    'home.html',
    { 'user': request.user }
    )