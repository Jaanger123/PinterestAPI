from django.contrib.auth import get_user_model
from rest_framework import views, status
from rest_framework.response import Response

from .serializers import RegisterSerializer

User = get_user_model()


class RegisterView(views.APIView):
	def post(self, request):
		data = request.data
		serializer = RegisterSerializer(data=data)

		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response('Successfully registered', status.HTTP_200_OK)


class ActivationView(views.APIView):
	def get(self, request, activation_code):
		user = User.objects.filter(activation_code=activation_code).first()

		if not user:
			return Response('This user does not exist', status.HTTP_400_BAD_REQUEST)
		user.activation_code = ''
		user.is_active = True
		user.save()
		return Response('Account successfully activated.', status.HTTP_200_OK)