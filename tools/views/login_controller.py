from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, logout, login as auth_login
from tools.models import UserProfile

"""
	login(request)
	View handler for the login page.
	Includes both displaying form and internally authenticating users.
"""
def login(request):
    #if the HTTP request method is POST, we know the login form was submitted
    if request.method == 'POST':
        #get the entered username and password from the request
        user_name = request.POST['user_name']
        password = request.POST['passwd']
        #attempt to auth the user
        user = authenticate(username=user_name, password=password)
        if user and user.is_active:
            #log in user in session if auth'd and user is active,
            #and return to the index page
            auth_login(request, user)
            return HttpResponseRedirect(reverse('tools:tools'))
        else:
            #otherwise, tell them login was invalid
            context = {'message': "Invalid login!"}
            return render(request, 'tools/login.html', context)
    else:
        #if not post, method is GET - the standard method for page browsing
        if 'a' in request.GET and request.GET['a'] == '1':
            #if ?a=1, log out and return user to index page
            logout(request)
            return HttpResponseRedirect(reverse('tools:tools'))
        else:
             #otherwise, just render the login form page
             return render(request, 'tools/login.html')
