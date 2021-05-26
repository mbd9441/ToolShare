import re
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from tools.models import UserProfile,Community

"""
	register(request)
	View handler for the user registration page.
	Handles both displaying the form and creating the new user.
"""
def register(request):
    if (request.method == 'POST'):
        #get the values entered in the form
        user_name = request.POST['user_name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        zip = request.POST['zip_code']
        passwd = request.POST['passwd']
        passwd2 = request.POST['passwd2']
        over18 = request.POST.get('over18')
        
        #strip whitespace
        user_name_check = user_name.strip()
        first_name_check = first_name.strip()
        last_name_check = last_name.strip()
        zip_check = zip.strip()
        passwd_check = passwd.strip()
        passwd2_check = passwd.strip()
       
        #validate input
        errors = 0
        message = [None] * 6
        if not ( isEmail(user_name) ):
            message[0] = "Email is not a valid email."
            errors+=1
        elif User.objects.filter(username=user_name):
            message[0] = "Email already exists!"
            errors+=1
        if not ( first_name_check ):
            message[1] = "First Name is blank."
            errors+=1
        if not ( last_name_check ):
            message[2] = "Last Name is blank."
            errors+=1
        if not ( isZip(zip) ):
            message[3] = "Zip is invalid."
            errors+=1
        if not ( passwd_check ):
            message[4] = "Password is blank."
            errors+=1
        if ( passwd != passwd2 ):
            message[4]= "Passwords do not match."
            errors+=1
        if not (over18):
            message[5] = "You are not over 18."
            errors+=1
        
        #create user if no errors
        if not ( errors ):
            #check community exists
            if (not Community.objects.filter(zip_code=zip)):
                c = Community(zip_code=zip)
                c.num_members = 0
                c.save()
            #create the user profile and save it to the database
            u = UserProfile(community=Community.objects.get(zip_code=zip))
            u.user = User.objects.create_user(user_name, user_name,passwd)
            u.user.first_name = first_name
            u.user.last_name = last_name
            u.user.save()
            u.save()
            return render(request, 'tools/login.html')
        #pass fields back on error.
        context = { 'over18':over18, 'user_name' : user_name, 'first_name' : first_name, 'last_name' : last_name, 'zip_code' : zip, 'message':message }
        return render(request, 'tools/register.html', context)
    return render(request, 'tools/register.html')

def isZip(str):
    i = 0;
    for u in list(str):
        if ( u.isdigit() ):
            i = i + 1
        else:
            return 0;
    if ( i == 5 ):
        return 1
    return 0

def isEmail(str):
    r = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not r.match(str):
        return 0
    return 1
