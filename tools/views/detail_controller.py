from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from tools.models import Tool,UserProfile,Rent,RentRequest

"""
	detail(request, tool_id)
	View handler for tool detail page
"""
def detail(request, tool_id):
    delete = None
    user = None
    rent = None
    if request.user.is_authenticated():
        tool = Tool.objects.filter(pk=tool_id)
        user_profile = UserProfile.objects.get(user=request.user)
        if len(tool) == 0:
            return HttpResponseRedirect(reverse('tools:tools'))
        else:
            tool = Tool.objects.get(pk=tool_id)
            if tool.owner.community == user_profile.community:
                request_list = RentRequest.objects.filter()
                tool_request_list = RentRequest.objects.filter(tool_requested = tool, req_status = 0)
                myrequest = RentRequest.objects.filter(requester = user_profile, tool_requested = tool, req_status = 0)
                if (tool.rentable == 0): 
                    checkrent = Rent.objects.filter(tool_rented = tool, returned = 0)
                    if len(checkrent) != 0:
                        rent = Rent.objects.get(tool_rented = tool, returned = 0)
                context = {'myrequest':myrequest, 'tool': tool, 'rent': rent, 'user': user_profile, 'request_list' : request_list, 'tool_request_list' : tool_request_list}
                return render(request, 'tools/detail.html', context)
            else:
                return HttpResponseRedirect(reverse('tools:tools'))
    return HttpResponseRedirect(reverse('tools:login'))