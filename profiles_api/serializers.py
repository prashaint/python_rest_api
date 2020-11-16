from rest_framework import serializers


class HelloApiSerializer(serializers.Serializer):
	"""Serializes the name field of our API view"""
	name = serializers.CharField(max_length=10)
