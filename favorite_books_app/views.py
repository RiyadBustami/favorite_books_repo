from django.http import HttpResponse
from django.shortcuts import render,redirect
from favorite_books_app.models import *
from django.contrib import messages
# Create your views here.
def show_books(request):
    if 'id' in request.session:
        context={
            'logged_user':User.objects.get(id=request.session['id']),
            'books':Book.objects.all().order_by('-id'),
        }
        return render(request, 'books.html',context)
    else:
        return redirect('/')

def add_book(request):
    if request.method == 'POST':
        errors=Book.objects.book_validator(request.POST)
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request,value)
        else:
            new_book=models_create_book(request)
    return redirect('/books/')

def show_book(request,book_id):
    context={
        'logged_user':User.objects.get(id=request.session['id']),
        'book':Book.objects.get(id=book_id)
    }
    return render(request,'show_book.html',context)

def add_book_to_favorites(request,book_id):
    models_add_book_to_favorites(request,book_id)
    return redirect('/books/'+str(book_id)+'/')


def update_book(request,book_id):
    if request.method == 'POST':
        errors=Book.objects.book_validator(request.POST)
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request,value)
        else:
            models_update_book(request,book_id)
    return redirect('/books/'+str(book_id)+'/')

def delete_book(request,book_id):
    if request.method == 'POST':
        models_delete_book(request,book_id)
        return redirect('/books/')
    return redirect('/books/'+str(book_id)+'/')

def unfavorite_book(request,book_id):
    if request.method == 'POST':
        models_unfavorite_book(request,book_id)
    return redirect('/books/')