from django.conf.urls import patterns, url
from tools.views import index_controller, detail_controller, login_controller, register_controller,list_controller, \
    renttool_controller, returntool_controller, userpage_controller, reviewuser_controller

urlpatterns = patterns('',
    url(r'^login', login_controller.login, name='login'),
    url(r'^$', index_controller.index, name="tools"),
    url(r'^(?P<tool_id>\d+)/$', detail_controller.detail, name='detail'),
    url(r'^register', register_controller.register, name='register'),
    url(r'^list', list_controller.list, name='list'),
    url(r'^rent', renttool_controller.renttool, name='rent'),
    url(r'^returntool', returntool_controller.returntool, name='returntool'),
    url(r'^user', userpage_controller.userpage, name='user'),
    url(r'^review', reviewuser_controller.reviewuser, name='review')
)
