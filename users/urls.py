from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import sign

urlpatterns = [
    path('users/token/refresh', TokenRefreshView.as_view()),
    path('users/signin', sign.UserSignInView.as_view()),
    path('users/signout', sign.UserSignOutView.as_view()),
]
