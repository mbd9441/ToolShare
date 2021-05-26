from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import User
from tools.models import Tool,UserProfile,Community,Rent,RentRequest

"""
        renttool(request)
        View handler for tool detail renting
        Handles renting of tool.
"""
def renttool(request):
    #validate user is logged in
    if request.user.is_authenticated():
        if request.method=='GET':
            if 'a' in request.GET:
                rentrequest = RentRequest.objects.get(pk=request.GET['r'])
                rented_tool = rentrequest.tool_requested
                rented_renter = rentrequest.requester
                if request.GET['a'] == '1':
                    if rented_tool.rentable == 1:
                        if rented_renter.canrent:
                            rentrequest.req_status = 1
                            rentrequest.save()
                            rent = Rent.objects.create(tool_rented = rented_tool, renter = rented_renter)
                            rent.returned = 0
                            rent.save()
                            rented_tool.rentable = 0
                            rented_tool.save()
                            print("accept")
                        else:
                            print("already renting max")
                elif request.GET['a'] == '0':
                    print("deny")
                    rentrequest.req_status = 2
                    rentrequest.save()
            else:
                #get ids from get
                renter_id = request.GET['u']
                tool_id = request.GET['t']
                #get objects from ids
                rent_tool = Tool.objects.get(pk=tool_id)
                rent_tool_owner = rent_tool.owner
                rent_renter = UserProfile.objects.get(user_id=renter_id)
                
                if rent_tool.rentable == 1:
                    req_list = RentRequest.objects.filter(requester = rent_renter, tool_requested = rent_tool, req_status = 0 )
                    if (len(req_list) == 0 ): #user does not have a request for the tool
                        if rent_renter.canrent:
                            print("renting tool")
                            rent_tool.save()
                            rent_request = RentRequest.objects.create( owner = rent_tool_owner, requester = rent_renter, tool_requested = rent_tool )
                            rent_request.save()
    return HttpResponseRedirect(reverse('tools:tools'))