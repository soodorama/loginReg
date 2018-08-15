from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    errors = {}
    if 'error' in request.session:
        if 'error' == 'email':
            errors = { 'error' : "No user with that email" }
        else:
            errors = { 'error' : 'Invalid login' }
    else:
        if 'logged_in' in request.session:
            return redirect(reverse('wall'))
    return render(request, 'login_reg/index.html', errors)

def login(request):
    email = request.POST['login_email']
    user_pw = request.POST['login_pw']
    user = User.objects.filter(email=email)
    if len(user):
        if bcrypt.checkpw(user_pw.encode(), user[0].password.encode()):
            request.session['first_name'] = user[0].first_name,
            request.session['logged_in'] = user[0].id
            request.session['success_message'] = "logged in"
            messages.success(request,"Successfully logged in")
            return redirect(reverse('wall'))
        else:
            request.session['error'] = "login"
    else:
        request.session['error'] = "email"
    return redirect(reverse('home'))

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key,value in errors.items():
            messages.error(request,value,extra_tags=key)
        return redirect(reverse('home'))
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['reg_email']
        password = request.POST['reg_pw']
        hashed_pw = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        user = User.objects.create(first_name=first_name,last_name=last_name,email=email,password=hashed_pw)
        request.session['first_name'] = user.first_name
        request.session['logged_in'] = user.id
        request.session['success_message'] = "registered"
        return redirect(reverse('wall'))
    return redirect(reverse('home'))

def success(request):
    return render(request, 'login_reg/success.html')

def logout(request):
    request.session.clear()
    return redirect(reverse('home'))

def wall(request):
    if 'logged_in' not in request.session:
        return redirect(reverse('home'))
    else:
        content = {
            'messages' : Message.objects.all()
        }
        return render(request, 'login_reg/wall.html', content)

def new_message(request):
    user = User.objects.get(id=request.session['logged_in'])
    message = Message.objects.create(message=request.POST['new_message'],user=user)
    print(message)
    return redirect(reverse('wall'))

def new_comment(request):
    user = User.objects.get(id=request.session['logged_in'])
    message = Message.objects.get(id=request.POST['message_id'])
    comment = Comment.objects.create(comment=request.POST['new_comment'],user=user,message=message)
    return redirect(reverse('wall'))