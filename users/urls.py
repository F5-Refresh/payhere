from django.urls import path

from users.views.signup import UserSignUpView

urlpatterns = [path('/signup', UserSignUpView.as_view())]
