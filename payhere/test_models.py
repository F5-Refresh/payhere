from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate


class LoginTestModel(APITestCase):

    '''로그인 테스트모델 작성

    Writer: 이동연
    Date: 2022-07-05

    각 테스트의 로그인 테스트를 담당합니다.
    '''

    def __init__(self, user=None):
        self.user = user

    # 요청에대한 로그인테스트와 response를 반환합니다.
    def login_user_case(self, *pk, view, url, method, data={}):
        request = getattr(APIRequestFactory(), method)(url, data=data)
        view = view
        force_authenticate(request, self.user)
        response = view(request, *pk)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        return response
