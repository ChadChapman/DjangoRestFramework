from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
#class-based views, refactor #3:
	url(r'^snippets/$', views.SnippetList.as_view()),
	url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
	url(r'^users/$', views.UserList.as_view()),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view())

# """
# #refactor #1:
# 	url(r'^snippets/$', views.snippet_list),
# 	url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
# """
]
#refactor #2:
urlpatterns = format_suffix_patterns(urlpatterns)