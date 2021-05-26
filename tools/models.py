from django.db import models
from django.contrib.auth.models import User

class Community(models.Model):
    zip_code = models.IntegerField()
    def num_members(self):
        member_list = UserProfile.objects.filter(community = self)
        return len(member_list)
    def __str__(self):
        return str(self.zip_code)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    community = models.ForeignKey(Community)
    sharer_rating = models.FloatField(default=0)
    sharer_rating_count = models.IntegerField(default=0)
    borrower_rating = models.FloatField(default=0)
    borrower_rating_count = models.IntegerField(default=0)
    def numrent(self):
        my_tool_list = Tool.objects.filter(owner = self)
        if len(my_tool_list) > 5:
            return 5
        else:
            return len(my_tool_list)
            
    def canrent(self):
        nrent = 0
        my_tool_list = Tool.objects.filter(owner = self)
        if len(my_tool_list) > 5:
            nrent = 5
        else:
            nrent = len(my_tool_list)
        my_rent_list = Rent.objects.filter(renter = self, returned = 0)
        if len(my_rent_list) < nrent:
            return 1
        else:
            return 0
 
    def __str__(self):
        return self.user.username
    
class Tool(models.Model):
    owner = models.ForeignKey(UserProfile)
    tool_name = models.CharField(max_length=30)
    tool_desc = models.CharField(max_length=512)
    TOOL_TYPE_CHOICES = (
            (0,"Powertool"),
            (1,"Construction"),
            (2,"Automotive"),
            (3,"Garden"),
            (4,"Other"),
            )
    tool_type = models.IntegerField(choices=TOOL_TYPE_CHOICES)
    def rentable_default():
        return 1
    rentable = models.BooleanField(default=rentable_default)
    def requested(self):
        request_list = RentRequest.objects.filter(tool_requested = self, req_status = 0)
        if len(request_list) > 0:
            return 1
        else:
            return 0
    def __str__(self):
        return self.tool_name

class Rent(models.Model):
    time_rented = models.DateTimeField(auto_now=True)
    time_returned = models.DateTimeField(null=True)
    tool_rented = models.ForeignKey(Tool)
    renter = models.ForeignKey(UserProfile)
    def returned_default():
        return 0
    returned = models.BooleanField(default=returned_default)
    def __str__(self):
        return self.renter.user.username + ' ' + self.tool_rented.tool_name

class todoReview(models.Model):
    time_created = models.DateTimeField(auto_now=True)
    todo_reviewee = models.ForeignKey(UserProfile, related_name='todo_reviewee')
    todo_reviewer = models.ForeignKey(UserProfile, related_name='todo_reviewer')
    todo_tool = models.ForeignKey(Tool, related_name = 'todo_tool')
    todo_review_type = models.BooleanField(default = 0)
    def __str__(self):
        return str(self.todo_reviewee) + '(' + str(self.todo_review_type) + ')' + str(self.todo_reviewer)

class Review(models.Model):
    time_reviewed = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default = 0)
    comment = models.CharField(max_length=512)
    reviewer = models.ForeignKey(UserProfile, related_name='reviewer')
    reviewee = models.ForeignKey(UserProfile, related_name='reviewee')
    review_type = models.BooleanField(default = 0)
    def __str__(self):
        return str(self.reviewee) + '(' + str(self.review_type) + ')' + ':' + str(self.rating)

class RentRequest(models.Model):
    req_time = models.DateTimeField(auto_now=True)
    dec_time = models.DateTimeField(null=True)
    owner = models.ForeignKey(UserProfile, related_name='owner')
    requester = models.ForeignKey(UserProfile, related_name='requester')
    STATUS_CHOICES = (
            (0,"Waiting for Response"),
            (1,"Approved"),
            (2,"Denied"),
            )
    req_status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    tool_requested = models.ForeignKey(Tool) 
    def tool_owner(self):
        return self.tool_requested.owner
    def __str__(self):
        return '<'+ str(self.req_time) + '> Tool: ' + str(self.tool_requested) + ' Status:' + str(self.req_status)

