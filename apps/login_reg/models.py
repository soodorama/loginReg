from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        if 'first_name' in postData:
            first = postData['first_name']
            if len(first) < 2 or bool(re.search(r'\d', first)):
                errors['first_name'] = "First name must be all letters and 2 or more characters"
        else:
            errors['first_name'] = "First name cannot be blank"

        if 'last_name' in postData:
            last = postData['last_name']
            if len(last) < 2 or bool(re.search(r'\d', last)):
                errors['last_name'] = "Last name must be all letters and 2 or more characters"
        else:
            errors['last_name'] = "Last name cannot be blank"
        
        if 'reg_email' in postData:
            email = postData['reg_email']
            if len(email) < 6 or not EMAIL_REGEX.match(email):
                errors['reg_email'] = "Invalid email"
        else:
            errors['reg_email'] = "Email cannot be blank"

        if 'reg_pw' in postData and 'confirm' in postData:
            pw = postData['reg_pw']
            if len(pw) < 8 or pw != postData['confirm']:
                errors['reg_pw'] = "Password must be more than 8 characters and match confirmation password"
        else:
            errors['reg_pw'] = "Password cannot be blank"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,related_name="messages")

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,related_name="comments")
    message = models.ForeignKey(Message,related_name="comments")