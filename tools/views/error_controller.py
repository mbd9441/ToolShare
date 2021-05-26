from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from tools.models import UserProfile

def error(request):
    if request.user.is_authenticated():
        
    return HttpResponseRedirect(reverse('tools:tools'))