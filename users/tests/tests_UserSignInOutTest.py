import json

from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken
from users.models import User


class UserSignInOutTest(APITestCase):
    '''로그인 로그아웃 test code

    Writer: 조병민
    Date: 2022-07-05

    '''

    def setUp(self):
        User.objects.create_user(email='test1234@gmail.com', nickname='test_user', password='A123a123!123')

    # [POST] - 로그인 후 jwt를 반환
    def test_success_signin_return_jwt(self):
        data = {'email': 'test1234@gmail.com', 'password': 'A123a123!123'}
        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        user = User.objects.get(email='test1234@gmail.com')
        token = OutstandingToken.objects.filter(user=user).all()[1]

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(token.token, response.data['refresh'])

    # [POST] - email을 잘못 입력 시 401 코드 반환
    def test_fail_signin_email_return_401(self):
        data = {'email': 'test1211134@gmail.com', 'password': 'A123a123!123'}
        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    # [POST] - password를 잘못 입력 시 401 코드 반환
    def test_fail_signin_password_return_401(self):
        data = {'email': 'test1234@gmail.com', 'password': 'A123a12aaa3!123'}
        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    # [POST] - 로그아웃 시 200 코드 반환
    def test_sucess_signout_refreshtoken_return_200(self):
        data = {'email': 'test1234@gmail.com', 'password': 'A123a123!123'}
        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        '''header 추가 시 주의 사항

        1. HTTP_ 접두사를 꼭 붙여야 한다.
        2. header 명은 대문자로 작성해야한다.
        '''
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        response = self.client.post(
            '/users/signout',
            data=json.dumps({'refresh': f'{refresh_token}'}),
            content_type='application/json',
            **headers,
        )
        user = User.objects.get(email='test1234@gmail.com')
        black_token = BlacklistedToken.objects.filter(token__user=user).order_by('-blacklisted_at').first().token.token

        self.assertEqual(response.status_code, 200)
        self.assertEqual(refresh_token, black_token)

    # [POST] - 로그아웃 시 잘못 된 access token으로 요청, 401코드 반환
    def test_sucess_signout_header_accesshtoken_return_401(self):
        data = {'email': 'test1234@gmail.com', 'password': 'A123a123!123'}
        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        '''header 추가 시 주의 사항

        1. HTTP_ 접두사를 꼭 붙여야 한다.
        2. header 명은 대문자로 작성해야한다.
        '''
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}false"}
        response = self.client.post(
            '/users/signout',
            data=json.dumps({'refresh': f'{refresh_token}'}),
            content_type='application/json',
            **headers,
        )
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['messages'][0]['token_class'], 'AccessToken')
        self.assertEqual(response.data['code'], 'token_not_valid')
