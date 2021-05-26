from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from tools.models import Tool,UserProfile,Community,RentRequest
    
"""
	index(request)
	View handler for tools index page
"""
def index(request):
    if request.user.is_authenticated():
        user_profile = UserProfile.objects.get(user=request.user)
        user_list = UserProfile.objects.filter(community=user_profile.community).order_by('user').exclude(user = user_profile.user)
        tool_list = Tool.objects.filter().order_by('-rentable', '-pk').exclude(owner=user_profile)
        request_list = RentRequest.objects.filter()
        context = {'tool_list': tool_list, 'user_list' : user_list, 'user': user_profile, 'request_list' : request_list}
        return render(request, 'tools/index.html', context)
    return render(request, 'tools/login.html', None)
