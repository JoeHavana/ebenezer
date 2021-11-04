from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import allauth.app_settings
from django.conf import settings

from core.users.api.serializers import *
from rest_framework.authtoken.models import Token

from core.users.models import User 


@api_view(['POST', ])
def registration_view(request):

	if request.method == 'POST':
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			user = serializer.save() # user = account
			data['response'] = "Successfully registered"
			data['email'] = user.email
			data['username'] = user.username
			token = Token.objects.get(user=user).key
			data['token'] = token
			return Response(data)
		else:
			data = serializer.errors
			return Response(data)


@api_view(['GET', ])
def users_list_api_view(request):
	users = User.objects.all()
	if users:
		#List ALL
		if request.method == 'GET':
			user_serializer = UsersSerializer(users, many=True)
			return Response(user_serializer.data, status=status.HTTP_200_OK)




@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def user_detail_api_view(request, pk=None):

	user = User.objects.filter(id=pk).first()
	
	if user:

		# LIST
		if request.method == 'GET': # and pk is not None:
			user_serializer = RegistrationSerializer(user)
			return Response(user_serializer.data, status=status.HTTP_200_OK)

		# UPDATE A SECTION
		elif request.method == 'PATCH':
			user_serializer = UsersSerializer(user, data=request.data)
			if user_serializer.is_valid():
				user_serializer.save()
				return Response(user_serializer.data, status=status.HTTP_200_OK)
			return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	return Response({"message": "There is not any user with that ID."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH',])
def update_user(request, pk=None):

	user = User.objects.filter(id=pk).first()

	if request.method == 'PATCH':
		user_serializer = UsersSerializer(user, data=request.data)
		if user_serializer.is_valid():
			user_serializer.save()
			return Response(user_serializer.data, status=status.HTTP_200_OK)
		return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
"""
		instance.username = validated_data.get('username', instance.username)
		instance.email = validated_data.get('email', instance.email)
		instance.password = validated_data.get('password', instance.password)
		instance.password2 = validated_data.get('password2', instance.password2)
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		instance.set_password(password)
		instance.save()
		return instance
"""