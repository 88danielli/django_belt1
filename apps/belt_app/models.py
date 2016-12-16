from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z]+')

# Create your models here.
class UserManager(models.Manager):
    def login(self, post):
        login_email = post['login_email']
        login_password = post['login_password']

        errors =[]

        user_list = User.objects.filter(email = login_email)

        if len(login_email) < 1:
            errors.append('Email is required')
        if len(login_password) < 1:
            errors.append('Password is required')
        if user_list:
            active_user = user_list[0]
            password = login_password.encode()
            if bcrypt.hashpw(password, active_user.pw_hash.encode()) == user_list[0].pw_hash :
                return (True, active_user)
            else:
                errors.append('Email and password do not match')
        else:
            errors.append('Email does not exist')
        return (False, errors)

    def register(self, post):
        name = post['name']
        alias = post['alias']
        email = post['email']
        password = post['password']
        confirm_password = post['password']
        birthday = post['birthday']

        errors = []
        user_list = User.objects.filter(email = email)
        if len(name) < 1:
            errors.append('Name is required')
        if len(name) < 3:
            errors.append('Name requires 2 or more characters')
        if not name_regex.match(name):
            errors.append('Name must only contain letters')
        if len(alias) < 1:
            errors.append('Alias is required')
        if len(alias) < 3:
            errors.append('Alias requires 2 or more characters')
        if not EMAIL_REGEX.match(email):
            errors.append('Email is invalid!')
        if user_list:
            errors.append('Email already exists!')
        if len(password) < 1:
            errors.append('Password is required')
        if len(password) < 8:
            errors.append('Password must have more than 8 characters')
        if password != confirm_password:
            errors.append('Passwords do not match!')
        if not birthday:
            errors.append('Birthday is required')
        if len(errors) > 0:
            return (False, errors)
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = self.create(name=name, alias=alias, email=email, pw_hash=pw_hash, birthday=birthday)
        return (True, user)

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    pw_hash = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class QuoteManager(models.Manager):
    def process_quote(self,post,user_id):
        author_name = post['author_name']
        quote_text = post['quote_text']
        errors = []
        if len(author_name) < 4:
            errors.append('Quoted by must be more than 3 characters')
        if len(quote_text) < 11:
            errors.append('Message must be more than 10 characters')
        if len(errors) > 0:
            return (False, errors)
        else:
            user = User.objects.get(id=user_id)
            verified_quote = self.create(author_name=author_name, quote_text=quote_text, user=user)
        return (True, verified_quote)

class Quote(models.Model):
    author_name = models.CharField(max_length=100)
    quote_text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    objects = QuoteManager()

class FavoriteManager(models.Manager):
    def process_favorite(self, user_id, quote_id):
        user = User.objects.get(id=user_id)
        quote = Quote.objects.get(id=quote_id)
        new_favorite = self.create(user=user, quote=quote)
        return (True, quote)


class Favorite(models.Model):
    user = models.ForeignKey(User)
    quote = models.OneToOneField(Quote)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FavoriteManager()
