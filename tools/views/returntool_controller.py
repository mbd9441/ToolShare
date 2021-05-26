from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from tools.models import Tool,UserProfile,Rent, RentRequest, todoReview

"""
        return(request)
        View handler for tool detail returning
        Handles returning of tool.
"""
def returntool(request):
    #validate user is logged in
    if request.user.is_authenticated():
        if request.method=='GET':
            #get ids from get
            renter = UserProfile.objects.get(pk=request.GET['u'])
            print(request.user.pk)
            tool_id = request.GET['t']
            #get objects from ids
            rent_tool = Tool.objects.get(pk=tool_id)
            if (rent_tool.rentable == 0):
                rent_renter = UserProfile.objects.get(user_id=request.user.pk)
                rent_rent = rent_renter.rent_set.get(tool_rented = rent_tool, renter=rent_renter, returned = 0)
                rent_request = RentRequest.objects.get(tool_requested=rent_tool, requester = renter, req_status = 1)
                if ( rent_rent ):
                    #update tool to not be rentable
                    rent_tool.rentable = 1
                    rent_tool.save()
                    
                    rent_request.delete()
                    
                    #update rent log
                    rent_rent.returned = 1
                    rent_rent.save()
                    
                    reviewa = todoReview.objects.create(todo_reviewee = rent_rent.tool_rented.owner, todo_reviewer = renter, todo_review_type = 0, todo_tool = rent_tool)
                    reviewb = todoReview.objects.create(todo_reviewee = renter, todo_reviewer = rent_rent.tool_rented.owner, todo_review_type = 1, todo_tool = rent_tool)
                    reviewa.save()
                    reviewb.save()
                    print(reviewa, reviewb)
                else:
                    print("add error message (request user != renter)")

    return HttpResponseRedirect(reverse('tools:tools'))
