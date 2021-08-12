from django.urls import path

from .views import RegisterView, ActivationView

urlpatterns = [
	path('register/', RegisterView.as_view()),
	path('activate/<str:activation_code>/', ActivationView.as_view(), name='activate')
]
