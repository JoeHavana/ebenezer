from rest_framework import serializers
from core.users.models import User

import allauth.app_settings
from django.conf import settings


class UsersSerializer(serializers.ModelSerializer):
	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	class Meta:
		model = User
		exclude = ['country']
		extra_kwargs = {
			'password': {'write_only': True}
		}


# CodingWithMitch Cap .6
class RegistrationSerializer(serializers.ModelSerializer):

	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'password2']
		extra_kwargs = {
			'password': {'write_only': True}
		}

	def save(self, validated_data):	# TODO: Originally save()
		user = User( # Account
			email=self.validated_data['email'],
			username=self.validated_data['username']
		)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']

		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		user.set_password(password)
		user.save()
		return user

	def update(self, instance, validated_data):
		instance.username = validated_data.get('username', instance.username)
		instance.email = validated_data.get('email', instance.email)
		instance.password = validated_data.get('password', instance.password)
		instance.password2 = validated_data.get('password2', instance.password2)
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		instance.set_password(password)
		instance.save()
		return instance