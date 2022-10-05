from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from login_registration_app.models import User
import bcrypt

# Create your views here.


def index(request):
    if 'id' in request.session:
        return redirect('success/')
    else:
        return render(request, "index.html")


def success(request):
    if 'id' in request.session:
        context={
            'logged_user':User.objects.get(id=request.session['id'])
        }
        return redirect('/books/')
    else:
        return redirect('/')


def logout(request):
    if 'id' in request.session:
        del request.session['id']
        return redirect('/')
    else:
        return redirect('/')


def process(request):
    if request.method == 'POST':
        if request.POST['source'] == 'reg':
            errors = User.objects.user_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/')
            else:
                try:
                    User.objects.get(email=request.POST['email'])
                except:
                    fname_tobe = str(request.POST['first_name']).capitalize()
                    lname_tobe = str(request.POST['last_name']).capitalize()
                    email_tobe = request.POST['email']
                    password_tobe = request.POST['password']
                    hashed_password = bcrypt.hashpw(
                        str(password_tobe).encode(), bcrypt.gensalt()).decode()
                    request.session['id'] = User.objects.create(
                        first_name=fname_tobe, last_name=lname_tobe, email=email_tobe, password=hashed_password).id
                    return redirect('/success/')
                messages.error(
                    request, 'Email already registered, please login.')
                return redirect('/')

        elif request.POST['source'] == 'login':
            try:
                user_conf = User.objects.get(email=request.POST['email'])
            except:
                messages.error(
                    request, 'Email does not exist, please register.')
                return redirect('/')
            if bcrypt.checkpw(str(request.POST['password']).encode(), str(user_conf.password).encode()):
                request.session['id'] = user_conf.id
                return redirect('/success/')
            else:
                messages.error(request, 'Wrong Password')
                return redirect('/')

        else:
            return redirect('/')
    else:
        render(request, 'index.html')
