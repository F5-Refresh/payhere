from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import sign

urlpatterns = [
    path('/token/refresh', TokenRefreshView.as_view()),
    path('/signin', sign.UserSignInView.as_view()),
    path('/signout', sign.UserSignOutView.as_view()),
]
