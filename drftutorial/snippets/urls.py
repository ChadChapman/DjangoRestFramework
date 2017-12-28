from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
#
from snippets.views import SnippetViewSet, UserViewSet, api_root
from rest_framework import renderers

snippet_list = SnippetViewSet.as_view({
	'get': 'list'
	, 'post': 'create'
	})

snippet_detail = SnippetViewSet.as_view({
	'get': 'retrieve'
	, 'put': 'update'
	, 'patch': 'partial_update'
	, 'delete': 'destroy'
	})

snippet_highlight = SnippetViewSet.as_view({
	'get': 'highlight'
	}
	, renderer_classes=[renderers.StaticHTMLRenderer])

user_list = UserViewSet.as_view({
	'get': 'list'
	})

user_detail = UserViewSet.as_view({
	'get': 'retrieve'
	})

urlpatterns = [
# ViewSet based urls, refactor #4:
	url(r'^$', api_root)
	, url(r'^snippets/$', snippet_list, name='snippet-list')
	, url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail')

	, url(r'^users/$', user_list, name='user-list')
	, url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')

# """
# #class-based views, refactor #3:
# 	url(r'^$', views.api_root),
# 	url(r'^snippets/$', views.SnippetList.as_view(), name='snippet-list'),
# 	url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(), name='snippet-detail'),

# 	url(r'^users/$', views.UserList.as_view(), name='user-list'),
# 	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
	
# 	url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view(), name='snippet-highlight'),

# """
# """
# #refactor #1:
# 	url(r'^snippets/$', views.snippet_list),
# 	url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
# """
]
#refactor #2:
urlpatterns = format_suffix_patterns(urlpatterns)