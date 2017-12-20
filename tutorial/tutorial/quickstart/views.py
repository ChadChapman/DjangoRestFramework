from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer

# views here:

#API endpoint to allow editing and viewing of Users
class UserViewSet(viewset.ModelViewSet):
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

#API endpoint to allow editing and viewing of Groups
class GroupViewSet(viewset.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = GroupSerializer


