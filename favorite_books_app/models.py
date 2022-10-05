from django.db import models
from django.forms import CharField
from login_registration_app.models import User

# Create your models here.
class BookManager(models.Manager):
    def book_validator(self,postData):
        errors={}
        if not postData['title']:
            errors['title']='Title is required!;'
        if len(postData['desc'])<5:
            errors['desc']='Description should be more that 5 characters!'
        return errors

class Book(models.Model):
    title=models.CharField(max_length=255)
    desc=models.TextField(default="")
    users_who_like = models.ManyToManyField(User,related_name='liked_books')
    uploaded_by=models.ForeignKey(User,related_name='books_uploaded',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=BookManager()

def models_create_book(request):
    title=request.POST['title']
    desc=request.POST['desc']
    logged_user=User.objects.get(id=request.session['id'])
    new_book= Book.objects.create(title=title,desc=desc,uploaded_by=logged_user)
    new_book.users_who_like.add(logged_user)
    return new_book

def models_add_book_to_favorites(request,book_id):
    user=User.objects.get(id=request.session['id'])
    user.liked_books.add(Book.objects.get(id=book_id))
    
def models_update_book(request,book_id):
    tb_updated_book=Book.objects.get(id=book_id)
    title=request.POST['title']
    desc=request.POST['desc']
    tb_updated_book.title=title
    tb_updated_book.desc=desc
    tb_updated_book.save()

def models_delete_book(request,book_id):
    tb_deleted_book=Book.objects.get(id=book_id)
    tb_deleted_book.delete()

def models_unfavorite_book(request,book_id):
        logged_user=User.objects.get(id=request.session['id'])
        tb_unfv_book=Book.objects.get(id=book_id)
        logged_user.liked_books.remove(tb_unfv_book)
