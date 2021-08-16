from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import *
from .serializers import *
from .permissions import *


class CategoryViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

	def filter_queryset(self, queryset):
		queryset = super().filter_queryset(queryset)
		return queryset.order_by('title')

	def get_permissions(self):
		if self.action in ['create', 'destroy']:
			permissions = [IsAdminUser]
		else:
			permissions = [AllowAny]
		return [permission() for permission in permissions]

	@action(detail=False, methods=['get'])
	def search(self, request, pk=None):
		q = request.query_params.get('q')
		queryset = self.get_queryset()
		queryset = queryset.filter(Q(slug__icontains=q) | Q(title__icontains=q))
		serializer = CategorySerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class PinViewSet(ModelViewSet):
	queryset = Pin.objects.all()
	serializer_class = PinSerializer

	def filter_queryset(self, queryset):
		queryset = super().filter_queryset(queryset)
		return queryset.order_by('-created')

	def get_permissions(self):
		if self.action in ['update', 'partial_update', 'destroy']:
			permissions = [IsPostAuthor]
		else:
			permissions = [IsAuthenticated]
		return [permission() for permission in permissions]

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['action'] = self.action
		return context

	@action(detail=False, methods=['get'])
	def own(self, request, pk=None):
		queryset = Pin.objects.filter(author=request.user)
		serializer = PinSerializer(queryset, many=True)
		return Response(serializer.data, status.HTTP_200_OK)

	@action(detail=False, methods=['get'])
	def search(self, request, pk=None):
		q = request.query_params.get('q')
		queryset = self.get_queryset()
		queryset = queryset.filter(Q(title__icontains=q) | Q(text__icontains=q))
		serializer = PinSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

	def get_permissions(self):
		if self.action in ['update', 'partial_update', 'destroy']:
			permissions = [IsPostAuthor]
		else:
			permissions = [IsAdminUser]
		return [permission() for permission in permissions]


class RatingViewSet(ModelViewSet):
	queryset = Rating.objects.all()
	serializer_class = RatingSerializer

	def filter_queryset(self, queryset):
		queryset = super().filter_queryset(queryset)
		return queryset.order_by('author')

	def get_permissions(self):
		if self.action in ['update', 'partial_update', 'destroy']:
			permissions = [IsPostAuthor]
		elif self.action in ['create']:
			permissions = [IsAuthenticated]
		else:
			permissions = [IsAdminUser]
		return [permission() for permission in permissions]
