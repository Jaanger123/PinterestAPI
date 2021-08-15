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

	def get_permissions(self):
		if self.action in ['create', 'destroy']:
			permissions = [IsAdminUser]
		else:
			permissions = [AllowAny]
		return [permission() for permission in permissions]


class PinViewSet(ModelViewSet):
	queryset = Pin.objects.all()
	serializer_class = PinSerializer

	def get_permissions(self):
		if self.action in ['update', 'partial_update', 'destroy']:
			permissions = [IsPostAuthor]
		else:
			permissions = [IsAuthenticated]
		return [permission() for permission in permissions]

	@action(detail=False, methods=['get'])
	def own(self, request, pk=None):
		queryset = Pin.objects.filter(author=request.user)
		serializer = PinSerializer(queryset, many=True)
		return Response(serializer.data, status.HTTP_200_OK)


class CommentViewSet(ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

	def get_permissions(self):
		if self.action in ['update', 'partial_update', 'destroy']:
			permissions = [IsPostAuthor]
		else:
			permissions = [IsAuthenticated]
		return [permission() for permission in permissions]
