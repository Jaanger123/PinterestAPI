from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .utils import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(min_length=8, required=True, write_only=True)
	password_confirmation = serializers.CharField(min_length=8, required=True, write_only=True)

	class Meta:
		model = CustomUser
		fields = ['username', 'email', 'password', 'password_confirmation']

	def validate(self, attrs):
		password = attrs.get('password')
		password_conf = attrs.pop('password_confirmation')

		if password != password_conf:
			raise serializers.ValidationError('Passwords do not match')
		return attrs

	def create(self, validated_data):
		user = CustomUser.objects.create_user(**validated_data)
		send_activation_code(user.email, user.activation_code)
		return user


class LogoutSerializer(serializers.Serializer):
	refresh = serializers.CharField()

	def validate(self, attrs):
		self.token = attrs.get('refresh')
		return attrs

	def save(self, **kwargs):
		try:
			RefreshToken(self.token).blacklist()
		except TokenError:
			self.fail('Incorrect token')
