from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from tools.models import Tool,UserProfile,Community,Rent,RentRequest
    
"""
	list(request)
	View handler for tool listing page.
	Handles displaying listing form, creating the new tool & deleting tools.
"""
def list(request):
    user = None
    tool = None
    name_message = ''
    desc_message = ''
    alert_message = ''
    tool_id = None
    tool_name=''
    tool_desc=''
    tool_type_id=4
    rentable = 1
    #only show page if use is auth'd
    if request.user.is_authenticated():
        user_profile = UserProfile.objects.get(user=request.user)
        tool_list = Tool.objects.filter(owner = user_profile).order_by('-pk')
        request_list = RentRequest.objects.filter( )
        if request.method == 'GET':
            if 't' in request.GET:
                if 'a' in request.GET:
                    tool_id = request.GET['t']
                    tool = Tool.objects.get(pk=tool_id)
                    if request.GET['a'] == '0':
                        tool_name = tool.tool_name
                        tool_desc = tool.tool_desc
                        tool_type_id = tool.tool_type
                        rentable = tool.rentable
                    elif request.GET['a'] == '1':
                        if tool.owner == user_profile:
                            tool.delete()
                        return HttpResponseRedirect(reverse('tools:tools'))
        elif request.method=='POST':
            #get the tool information
            tool_id = request.POST.get('tool_id')
            if(tool_id):
                tool = Tool.objects.get(pk=tool_id)
            tool_name = request.POST['tool_name']
            name_check = tool_name.strip() #strip() gets rid of all whitespace
            
            tool_desc = request.POST['tool_desc']
            desc_check = tool_desc.strip() #strip() gets rid of all whitespace
            
            tool_type_id = int(request.POST.get('tool_types'))
            tool_type = Tool.TOOL_TYPE_CHOICES[int(tool_type_id)]
            
            rentable = request.POST.get('rentable')
            if not rentable:
                rentable = 0
            else:
                rentable = 1
            
            if not ((name_check) and (desc_check)) or (len(tool_name)>30 or len(tool_desc)>512): #are either of them empty?
                if not (name_check): #if name is empty
                    name_message = "Tool name is blank." 
                elif (len(tool_name)>30):
                    name_message = "Tool name is " + str(abs(30-len(tool_name))) + " characters longer than 30."
                if not (desc_check): #if desc is empty
                    desc_message = "Tool description is blank."
                elif (len(tool_desc)>512):
                    desc_message = "Tool description is " + str(abs(512-len(tool_desc))) + " characters longer than 512." 
            elif (tool):
                    #edits tool attributes and save
                    tool = Tool.objects.get(pk=tool_id)
                    tool.tool_name = tool_name
                    tool.tool_desc = tool_desc
                    tool.tool_type = tool_type_id
                    tool.rentable = rentable
                    tool.save()
                    
                    #display message for bottom of the screen
                    alert_message = (tool_name) + " Updated!"
            else:
                    #create the new tool with them as the owner
                    user_profile.tool_set.create(tool_name=tool_name, tool_desc=tool_desc, tool_type = tool_type_id, rentable = rentable)
                    #and save the tool to the database
                    user_profile.save()
                    
                    #display message for bottom of the screen
                    alert_message = (tool_name) + " Created!"
                    
                    #reset saved data so new tool can be created
                    user = None
                    tool = None
                    name_message = ''
                    desc_message = ''
                    tool_id = None
                    tool_name=''
                    tool_desc=''
                    tool_type_id=4
                    rentable = 1
 
        context = {'rentable':rentable, 'request_list':request_list, 'tool_list':tool_list, 'alert_message':alert_message, 'tool_id':tool_id, 'tool_name':tool_name, 'tool_desc':tool_desc, 'tool_type_id':tool_type_id, 'tool':tool, 'desc_message':desc_message, 'name_message':name_message, 'user' : user_profile, 'tool_types' : Tool.TOOL_TYPE_CHOICES  }
        return render(request, 'tools/list.html', context)
    return HttpResponseRedirect(reverse('tools:login'))
