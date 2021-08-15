from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'


class PinSerializer(serializers.ModelSerializer):
	author = serializers.ReadOnlyField(source='author.username')
	created = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

	class Meta:
		model = Pin
		fields = '__all__'

	def to_representation(self, instance):
		representation = super().to_representation(instance)
		action = self.context.get('action')

		if action == 'list':
			representation['comments'] = instance.comments.count()
		elif action == 'retrieve':
			representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
		return representation

	def create(self, validated_data):
		request = self.context.get('request')
		pin = Pin.objects.create(author=request.user, **validated_data)
		return pin


class CommentSerializer(serializers.ModelSerializer):
	author = serializers.ReadOnlyField(source='author.username')
	created = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

	class Meta:
		model = Comment
		fields = '__all__'

	def create(self, validated_data):
		request = self.context.get('request')
		comment = Comment.objects.create(author=request.user, **validated_data)
		return comment
