from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from tools.models import Tool,UserProfile,Community,Rent,RentRequest, todoReview, Review

"""
        renttool(request)
        View handler for tool detail renting
        Handles renting of tool.
"""
def reviewuser(request):
    #validate user is logged in
    if request.user.is_authenticated():
        user_profile = UserProfile.objects.get(user=request.user)
        num_list = [1,2,3,4,5]
        todo_review_id = None
        todo_review = None
        todo_tool = None
        review_type = None
        reviewer = None
        reviewee = None
        rating = 1
        comment = ''
        comment_message = ''
        
        if request.method=='GET':
            if not 'r' in request.GET:
                return HttpResponseRedirect(reverse('tools:tools'))
            else:
                #get ids from get
                todo_review_id = request.GET['r']
                todo_review = todoReview.objects.get(pk = todo_review_id)
                todo_tool = todo_review.todo_tool
                reviewee = todo_review.todo_reviewee

        elif request.method=='POST':
            todo_review_id = request.POST.get('todo_review_id')
            if todo_review_id:
                try_todo = todoReview.objects.filter(pk = todo_review_id)
                if try_todo:
                    todo_review = todoReview.objects.get(pk = todo_review_id)
            review_type = todo_review.todo_review_type
            reviewer = todo_review.todo_reviewer
            reviewee = todo_review.todo_reviewee
            rating = int(request.POST.get('rating'))
            comment = request.POST.get('comment')
            comment_check = comment.strip() #strip() gets rid of all whitespace
            
            if not (comment_check): #if name is empty
                comment_message = "Comment is blank." 
            elif (len(comment_check)>512):
                comment_message = "Comment is " + str(abs(512-len(comment))) + " characters longer than 30."
            else:
                review = Review.objects.create(rating = rating, comment = comment, reviewer = reviewer, reviewee = reviewee, review_type = review_type )
                review.save()
                
                if review_type:
                    dborrow_count = reviewee.borrower_rating_count
                    dborrow_rating = reviewee.borrower_rating
                
                    dborrow_rating = dborrow_rating*dborrow_count
                    dborrow_rating = dborrow_rating+rating
                    dborrow_count = dborrow_count+1
                    dborrow_rating = dborrow_rating/dborrow_count
                    
                    reviewee.borrower_rating_count = dborrow_count
                    reviewee.borrower_rating = dborrow_rating
                else:
                    dshare_count = reviewee.sharer_rating_count
                    dshare_rating = reviewee.sharer_rating
                
                    dshare_rating = dshare_rating*dshare_count
                    dshare_rating = dshare_rating+rating
                    dshare_count = dshare_count+1
                    dshare_rating = dshare_rating/dshare_count
                    
                    reviewee.sharer_rating_count = dshare_count
                    reviewee.sharer_rating = dshare_rating 
                    
                reviewee.save()
                todo_review.delete()
                return HttpResponseRedirect(reverse('tools:tools'))

        context = {'rating':rating, 'comment':comment, 'comment_message':comment_message, 'todo_review_id':todo_review_id, 'num_list':num_list, 'todo_review':todo_review, 'reviewee':reviewee, 'user':user_profile}
        return render(request, 'tools/review.html', context)
    return HttpResponseRedirect(reverse('tools:tools'))
