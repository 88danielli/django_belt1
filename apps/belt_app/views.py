from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from . import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z]+')

def index(request):
    if not 'active_user' in request.session:
        request.session['active_user'] = ""
    return render(request, 'belt_app/index.html')

def quotes(request):
    if request.session['active_user'] == "" or not 'active_user' in request.session:
        messages.add_message(request, messages.ERROR, "Please Login to Continue")
        return redirect('/')
    else:
        quotes = models.Quote.objects.exclude(favorite__user__id=request.session['active_user']['id'])
        favorites = models.Favorite.objects.all()
        context = {
            'quotes': quotes,
            'favorites': favorites,
        }
        return render(request, 'belt_app/quotes.html', context)

def add_user(request):
    result = models.User.objects.register(request.POST)
    if result[0] == False:
        print result[1]
        for i in result[1]:
            messages.add_message(request, messages.ERROR, i)
        return redirect('/')
    else:
        print result[1]
        return log_user_in(request, result[1])
    return redirect('/quotes')

def login(request):
    result = models.User.objects.login(request.POST)
    if result[0] == False:
        for i in result[1]:
            messages.add_message(request, messages.ERROR, i)
        return redirect('/')
    else:
        return log_user_in(request, result[1])

def log_user_in(request, user):
    request.session['active_user'] = {
        'id' : user.id,
        'name' : user.name,
        'alias' : user.alias,
        'email' : user.email,
    }
    return redirect ('/quotes')

def logout(request):
    del request.session['active_user']
    return redirect('/')

# End of Login ***** Start of Quotes

def quote_process(request):
    result = models.Quote.objects.process_quote(request.POST,request.session['active_user']['id'])
    if result[0] == False:
        for i in result[1]:
            messages.add_message(request, messages.ERROR, i)
    return redirect ('/quotes')

def users(request, id):
    user = models.User.objects.filter(id=id)
    display_user = user[0]
    print user, "*"*50
    quotes_list = models.Quote.objects.filter(user_id=user[0].id)
    count = quotes_list.count()
    print quotes_list, "1"*50, count
    context={
    'quotes_list': quotes_list,
    'count': count,
    'user':display_user,
    }
    return render(request, 'belt_app/users.html', context)

def favorite_process(request, id):

    result = models.Favorite.objects.process_favorite(request.session['active_user']['id'],id)
    return redirect('/quotes')

def remove_favorite(request, id):
    result = models.Favorite.objects.remove_favorite(request.session['active_user']['id'],id)
    result[1].delete()
    return redirect('/quotes')
