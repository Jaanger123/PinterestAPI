from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'


class PinSerializer(serializers.ModelSerializer):
	author = serializers.ReadOnlyField(source='author.username')

	class Meta:
		model = Pin
		fields = ['id', 'author', 'category', 'title', 'text', 'image', 'link']

	def to_representation(self, instance):
		representation = super().to_representation(instance)
		return representation

	def create(self, validated_data):
		request = self.context.get('request')
		pin = Pin.objects.create(author=request.user, **validated_data)
		return pin


class CommentSerializer(serializers.ModelSerializer):
	author = serializers.ReadOnlyField(source='author.username')

	class Meta:
		model = Comment
		fields = ['id', 'author', 'pin', 'text']

	def create(self, validated_data):
		request = self.context.get('request')
		pin = Pin.objects.create(author=request.user, **validated_data)
		return pin
