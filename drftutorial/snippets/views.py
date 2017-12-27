
#never quite sure if tutorial mentions all lines to be deleted or not?

#generic class-based views:
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics
#
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
"""
#with mixins and generics:
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics
"""

"""
class-based refactor:
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
"""

"""
#refactor #1
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
"""

"""
#JSON only group
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
"""

#with generic class-based views:
class SnippetList(generics.ListCreateAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	#create() of serializer now passes owner field also
	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)


"""
#with mixins and generics:
class SnippetList(mixins.ListModelMixin
					, mixins.CreateModelMixin
					, generics.GenericAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

"""
"""	
#now onto class-based views:
class SnippetList(APIView):
	#list all code snippets or create a new one
	def get(self, request, format=None):
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = SnippetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
###

#first refactor on how to refine views:
#using api_view decorators now instead of csrf_exempt
"""
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
	#list all code snipets or create a new one
	if request.method == 'GET':
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = SnippetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
"""
first way I did it is below:
JSON was the only content type used

@csrf_exempt #bad idea normally but bearing with the tut for now
def snippet_list(request):
	#list all code snipets or create a new one
	if request.method == 'GET':
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = SnippetSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)
	###
"""

#using generic class-based views:
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

"""
#using mixins and generics:
class SnippetDetail(mixins.RetrieveModelMixin
					, mixins.UpdateModelMixin
					, mixins.DestroyModelMixin
					, generics.GenericAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

"""
"""
#using class-based view:

class SnippetDetail(APIView):
	#retrieve, update, or delete a snippet instance
	def get_object(self, pk):
		try:
			return Snippet.objects.get(pk=pk)
		except Snippet.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = SnippetSerializer(snippet)
		return Response(serializer.data)


	def put(self, request, format=None):
		snippet = self.get_object(pk)
		serializer = SnippetSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, format=None):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTEXT)
"""



#first refactor for refine in views
"""
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
	#return, update or delete an individual Snippet
	
	try:
		snippet = Snippet.objects.get(pk=pk)
	except Snippet.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = SnippetSerializer(snippet)
		return Response(serializer.data)

	elif request.method == 'PUT':
		serializer = SnippetSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTEXT)
"""
#first way I did it is below:
#JSON was the only content type used
"""
@csrf_exempt
def snippet_detail(request, pk):
	#return, update or delete an individual Snippet
	try:
		snippet = Snippet.objects.get(pk=pk)
	except Snippet.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = SnippetSerializer(snippet)
		return JsonResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = SnippetSerializer(snippet, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		snippet.delete()
		return HttpResponse(status=204)
"""

class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer