from rest_framework import serializers, status

from .models import *
from .utils import get_rating


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
		representation['likes'] = instance.likes.count()
		representation['rating'] = get_rating(representation.get('id'), Pin)

		if action == 'list':
			representation.pop('text')
			representation.pop('link')
			representation['comments'] = instance.comments.count()
		elif action == 'retrieve':
			representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
			queryset = Pin.objects.filter(category=instance.category)
			representation['similar'] = PinSerializer(queryset, many=True).data

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


class RatingSerializer(serializers.ModelSerializer):
	author = serializers.ReadOnlyField(source='author.username')

	class Meta:
		model = Rating
		fields = '__all__'

	def create(self, validated_data):
		request = self.context.get('request')
		user = request.user
		pin = validated_data.get('pin')

		if Rating.objects.filter(author=user, pin=pin):
			rating = Rating.objects.get(author=user, pin=pin)
			return rating

		rating = Rating.objects.create(author=request.user, **validated_data)
		return rating


class LikeSerializer(serializers.ModelSerializer):
	author = serializers.ReadOnlyField(source='author.username')

	class Meta:
		model = Like
		fields = '__all__'

	def create(self, validated_data):
		request = self.context.get('request')
		user = request.user
		pin = validated_data.get('pin')

		if Like.objects.filter(author=user, pin=pin):
			like = Like.objects.get(author=user, pin=pin)
			return like

		like = Like.objects.create(author=user, **validated_data)
		return like
