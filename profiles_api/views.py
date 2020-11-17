from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import filters
from rest_framework import viewsets
from profiles_api import models
from profiles_api import permissions
from profiles_api import serializers

class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloApiSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""

        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})
        
    def post(self, request):
    	"""Create a Hello message with our name"""
    	serializer = self.serializer_class(data=request.data)

    	if serializer.is_valid():
    		name = serializer.validated_data.get('name')
    		message = f'Hello {name} !!!'
    		return Response({'message': message})
    	else:
    		return Response(
    			serializer.errors,
    			status = status.HTTP_400_BAD_REQUEST
    			)

    def put(self, request, pk=None):
    	"""Puts a new object in place of pk object"""
    	return Response({'method':'PUT'})

    def patch(self, request, pk=None):
    	"""Updates the given object with given field values"""
    	return Response({'method':'PATCH'})

    def delete(self, request, pk=None):
    	"""Deletes the given object"""
    	return Response({'method':'DELETE'})


class HelloViewSet(viewsets.ViewSet):
	"""Test API viewset"""
	serializer_class = serializers.HelloApiSerializer


	def list(self, request):
		"""Returns a Hello Message"""

		a_viewset = [
			'Uses actions (list, create, retrieve, update, partial_update, destroy)',
			'Automatically Maps to URLs using Routers',
			'Provides more functionality with less code',
		]

		return Response({'message': 'Hello!', 'a_viewset':a_viewset})

	def create(self, request):
		"""Creates a new object"""
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			name = serializer.validated_data.get('name')
			message = f'Hello {name} $$'
			return Response({'message': message})
		else:
			return Response(
					serializer.errors,
					status=status.HTTP_400_BAD_REQUEST
				)


	def retrieve(self, request, pk=None):
		"""Retrieves the object by it's ID"""
		return Response({'http_method': 'GET'})

	def update(self, request, pk=None):
		"""Updates the object by it's ID"""
		return Response({'http_method': 'POST'})

	def partial_update(self, request, pk=None):
		"""Updates a part of data in the object by it's ID"""
		return Response({'http_method': 'PATCH'})

	def destroy(self, request, pk=None):
		"""Deletes the object by it's ID"""
		return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
	"""Creates and updates a user profile"""
	serializer_class = serializers.UserProfileSerializer
	queryset = models.UserProfile.objects.all()
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.UpdateOwnProfile,)
	filter_backends = (filters.SearchFilter,)
	search_fields = ('name','email',)

class UserLoginApiView(ObtainAuthToken):
	"""Creates user auth tokens"""
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
	"""Creates updates and views the user profile feeds"""
	authentication_classes = (TokenAuthentication,)
	serializer_class = serializers.ProfileFeedItemSerializer
	queryset = models.ProfileFeedItem.objects.all()
	permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

	def perform_create(self, serializer):
		"""Sets the user profile to the logged in user"""
		serializer.save(user_profile=self.request.user)


