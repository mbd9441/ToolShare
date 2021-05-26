from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from tools.models import UserProfile, Tool, Review, RentRequest, Rent, todoReview

"""
	user(request, user_id)
	View handler for tool detail page
"""
def userpage(request):
    #validate user is logged in
    if request.user.is_authenticated():
        if request.method=='GET':
            #get ids from get
            user_id = request.GET['u']
            #get objects from ids
            req_user = UserProfile.objects.filter(pk=user_id)
            if len(req_user) == 0:
                return HttpResponseRedirect(reverse('tools:tools'))
            else:
                req_user = UserProfile.objects.get(pk=user_id)
                user_profile = UserProfile.objects.get(user=request.user)
                if req_user.community == user_profile.community:
                    isownpage = req_user == user_profile
                    tool_list = Tool.objects.filter(owner = req_user).order_by('-pk')
                    rent_list = Rent.objects.filter(renter = req_user, returned = 0)
                    my_request_list = RentRequest.objects.filter(requester = req_user)
                    
                    todo_reviews = todoReview.objects.filter(todo_reviewer = req_user).order_by('-pk')
                    print(todo_reviews)
                    btool_list = []
                    for rent in rent_list:
                        btool_list.append(rent.tool_rented)
                    review_list = Review.objects.filter(reviewee=req_user).order_by('review_type', '-rating')
                    request_list = RentRequest.objects.filter(tool_requested__owner = user_profile, req_status = 0)
                    borrower_rating = format(req_user.borrower_rating, '.1f')
                    sharer_rating = format(req_user.sharer_rating, '.1f')
                    context = { 'sharer_rating':sharer_rating, 'borrower_rating': borrower_rating, 'todo_reviews':todo_reviews, 'status_choices':RentRequest.STATUS_CHOICES, 'my_request_list' : my_request_list, 'btool_list': btool_list, 'request_list':request_list, 'isownpage':isownpage, 'tool_list' : tool_list, 'review_list' : review_list, 'user' : user_profile, 'req_user' : req_user }
                    return render(request, 'tools/user.html', context)
                else:
                    return HttpResponseRedirect(reverse('tools:tools'))
    return HttpResponseRedirect(reverse('tools:login'))
        