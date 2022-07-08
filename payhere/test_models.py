from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from rest_framework import status

class TestModel(APITestCase):

    def __init__(self, user=None):
        self.user = user
    
    def login_user_case(self, *pk, view, url, method , data={}):
        request = getattr(APIRequestFactory(), method)(url, data=data)
        view = view
        force_authenticate(request, self.user)
        response = view(request, *pk)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        return response
