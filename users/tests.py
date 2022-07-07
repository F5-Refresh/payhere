import json

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken

from users.models import User


class UserSignUpTest(APITestCase):
    """회원가입 구현 View

    Writer: 김동규
    Date: 2022-07-05

    유저 회원가입의 성공/실패 경우를 테스트 합니다.

    param :
        email       - 이메일 주소
        nickname    - 닉네임
        password    - 비밀번호
    """

    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email='test02@gmail.com', nickname='DGK02', password='DGKtest12345!!')

    # success test
    def test_success_user_signup(self):
        data = {'email': 'test01@gmail.com', 'nickname': 'DGK01', 'password': 'DGKtest12345!!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json(), {'email': 'test01@gmail.com', 'nickname': 'DGK01'})

    # fail test
    def test_fail_user_signup_due_to_email_format_validation(self):
        data = {'email': 'test01@gmail', 'nickname': 'DGK01', 'password': 'DGKtest12345!!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'email': ['올바른 이메일 주소를 입력하세요.']})

    def test_fail_user_signup_due_to_already_existed_email(self):
        data = {'email': 'test02@gmail.com', 'nickname': 'DGK01', 'password': 'DGKtest12345!!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'email': ['user의 email은/는 이미 존재합니다.']})

    def test_fail_user_signup_due_to_email_required(self):
        data = {'nickname': 'DGK01', 'password': 'DGKtest12345!!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'email': ['필수 항목입니다.']})

    def test_fail_user_signup_due_to_already_existed_email_n_nickname(self):
        data = {'email': 'test02@gmail.com', 'nickname': 'DGK02', 'password': 'DGKtest12345!!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {'email': ['user의 email은/는 이미 존재합니다.'], 'nickname': ['user의 nickname은/는 이미 존재합니다.']}
        )

    def test_fail_user_signup_due_to_nickname_required(self):
        data = {'email': 'test01@gmail.com', 'password': 'DGKtest12345!!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'nickname': ['필수 항목입니다.']})

    def test_fail_user_signup_due_to_already_existed_nickname(self):
        data = {'email': 'test01@gmail.com', 'nickname': 'DGK02', 'password': 'DGKtest12345!!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'nickname': ['user의 nickname은/는 이미 존재합니다.']})

    def test_fail_user_signup_due_to_password_gt_20_digit(self):
        data = {
            'email': 'test01@gmail.com',
            'nickname': 'DGK01',
            'password': 'DGKtest12345!!DGKtest12345!!',
        }

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['올바른 비밀번호를 입력하세요.']})

    def test_fail_user_signup_due_to_password_lt_8_digit(self):
        data = {
            'email': 'test01@gmail.com',
            'nickname': 'DGK01',
            'password': 'DGKtest',
        }

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['올바른 비밀번호를 입력하세요.']})

    def test_fail_user_signup_due_to_password_required(self):
        data = {'email': 'test01@gmail.com', 'nickname': 'DGK01'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['필수 항목입니다.']})

    def test_fail_user_signup_due_to_password_no_small_letters(self):
        data = {
            'email': 'test01@gmail.com',
            'nickname': 'DGK01',
            'password': 'DGKTEST123!!',
        }

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['올바른 비밀번호를 입력하세요.']})

    def test_fail_user_signup_due_to_password_no_capital_letters(self):
        data = {
            'email': 'test01@gmail.com',
            'nickname': 'DGK01',
            'password': 'dgktest123!!',
        }

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['올바른 비밀번호를 입력하세요.']})

    def test_fail_user_signup_due_to_password_no_special_letters(self):
        data = {
            'email': 'test01@gmail.com',
            'nickname': 'DGK01',
            'password': 'DGKtest123',
        }

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['올바른 비밀번호를 입력하세요.']})

    def test_fail_user_signup_due_to_password_unexpected_special_letters(self):
        data = {
            'email': 'test01@gmail.com',
            'nickname': 'DGK01',
            'password': 'DGKtest123!!./',
        }

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['올바른 비밀번호를 입력하세요.']})


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
