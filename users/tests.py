import json

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken

from users.models import User


class UserSignInOutTest(APITestCase):
    def setUp(self):
        User.objects.create_user(email='test1234@gmail.com', nickname='test_user', password='A123a123!123')

    def test_given_email_password_then_requesting_signin_return_jwt(self):
        '''signit test code

        Writer: 조병민
        Date: 2022-07-05

        signin 요청하여 token을 발급

        ok_condition
            - status_code == 200
            - response: refresh token == 해당 유저의 OutstandingToken: refresh token
        '''
        data = {'email': 'test1234@gmail.com', 'password': 'A123a123!123'}
        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        user = User.objects.get(email='test1234@gmail.com')
        token = OutstandingToken.objects.filter(user=user).all()[1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(token.token, response.json()['refresh'])

    def test_given_refreshtoken_then_requesting_signout_return_200ok(self):
        '''signout test code

        Writer: 조병민
        Date: 2022-07-05

        signin 요청하여 token을 발급
        signout 요청하여 token 폐기

        ok_condition
            - status_code == 200
            - refresh_token == 해당 유저의 가장 마지막 BlackListToken: token.token
        '''

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
