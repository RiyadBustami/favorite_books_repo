from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self,postData):
        errors={}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        PWD_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$")
        NAME_REGEX =re.compile(r"\b([A-ZÀ-ÿ][-,a-z. ']+[ ]*)+") 
        if not NAME_REGEX.match(str(postData['first_name']).capitalize()):
            errors['first_name'] = "First Name REQUIRED; Longer than 2 characters."
        if not NAME_REGEX.match(str(postData['last_name']).capitalize()):
            errors['last_name'] = "Last Name REQUIRED; Longer than 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Not a valid email."
        if not PWD_REGEX.match(postData['password']):
            errors['password'] = "Password - required; at least 8 characters; has 1 num at least;"
        if postData['password_conf']!=postData['password']:
            errors['password_conf'] = "Password Confirmation doesn't match"

        return errors
        
        
class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    password=models.CharField(max_length=255)
    objects=UserManager()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)