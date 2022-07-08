import json

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken
from users.models import User


class UserSignUpTest(APITestCase):
    '''회원가입 구현 Test

    Writer: 김동규
    Date: 2022-07-05

    유저 회원가입의 성공/실패 경우를 테스트 합니다.
    '''

    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email='test02@gmail.com', nickname='DGK02', password='DGKtest12345!!')

    # [POST] - 유저 회원가입 성공 테스트
    def test_success_user_signup(self):
        data = {'email': 'test01@gmail.com', 'nickname': 'DGK01', 'password': 'DGKtest12345!!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json(), {'email': 'test01@gmail.com', 'nickname': 'DGK01'})

    # [POST] - 유저 회원가입 실패 테스트(이메일 형식)
    def test_fail_user_signup_due_to_email_format_validation(self):
        data = {'email': 'test01@gmail', 'nickname': 'DGK01', 'password': 'DGKtest12345!!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'email': ['유효한 이메일 주소를 입력하십시오.']})

    # [POST] - 유저 회원가입 실패 테스트(이미 존재하는 이메일)
    def test_fail_user_signup_due_to_already_existed_email(self):
        data = {'email': 'test02@gmail.com', 'nickname': 'DGK01', 'password': 'DGKtest12345!!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'email': ['user의 email은/는 이미 존재합니다.']})

    # [POST] - 유저 회원가입 실패 테스트(이메일 파라미터 존재X)
    def test_fail_user_signup_due_to_email_required(self):
        data = {'nickname': 'DGK01', 'password': 'DGKtest12345!!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'email': ['이 필드는 필수 항목입니다.']})

    # [POST] - 유저 회원가입 실패 테스트(이미 존재하는 이메일, 닉네임)
    def test_fail_user_signup_due_to_already_existed_email_n_nickname(self):
        data = {'email': 'test02@gmail.com', 'nickname': 'DGK02', 'password': 'DGKtest12345!!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {'email': ['user의 email은/는 이미 존재합니다.'], 'nickname': ['user의 nickname은/는 이미 존재합니다.']}
        )

    # [POST] - 유저 회원가입 실패 테스트(닉네임 파라미터 존재X)
    def test_fail_user_signup_due_to_nickname_required(self):
        data = {'email': 'test01@gmail.com', 'password': 'DGKtest12345!!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'nickname': ['이 필드는 필수 항목입니다.']})

    # [POST] - 유저 회원가입 실패 테스트(이미 존재하는 닉네임)
    def test_fail_user_signup_due_to_already_existed_nickname(self):
        data = {'email': 'test01@gmail.com', 'nickname': 'DGK02', 'password': 'DGKtest12345!!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'nickname': ['user의 nickname은/는 이미 존재합니다.']})

    # [POST] - 유저 회원가입 실패 테스트(패스워드 20자리 초과)
    def test_fail_user_signup_due_to_password_gt_20_digit(self):
        data = {
            'email': 'test01@gmail.com',
            'nickname': 'DGK01',
            'password': 'DGKtest12345!!DGKtest12345!!',
        }

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['올바른 비밀번호를 입력하세요.']})

    # [POST] - 유저 회원가입 실패 테스트(패스워드 8자리 미만)
    def test_fail_user_signup_due_to_password_lt_8_digit(self):
        data = {
            'email': 'test01@gmail.com',
            'nickname': 'DGK01',
            'password': 'DGKtest',
        }

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['올바른 비밀번호를 입력하세요.']})

    # [POST] - 유저 회원가입 실패 테스트(패스워드 파라미터 존재X)
    def test_fail_user_signup_due_to_password_required(self):
        data = {'email': 'test01@gmail.com', 'nickname': 'DGK01'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['이 필드는 필수 항목입니다.']})

    # [POST] - 유저 회원가입 실패 테스트(패스워드 형식 에러:소문자X)
    def test_fail_user_signup_due_to_password_no_small_letters(self):
        data = {
            'email': 'test01@gmail.com',
            'nickname': 'DGK01',
            'password': 'DGKTEST123!!',
        }

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['올바른 비밀번호를 입력하세요.']})

    # [POST] - 유저 회원가입 실패 테스트(패스워드 형식 에러:대문자X)
    def test_fail_user_signup_due_to_password_no_capital_letters(self):
        data = {
            'email': 'test01@gmail.com',
            'nickname': 'DGK01',
            'password': 'dgktest123!!',
        }

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['올바른 비밀번호를 입력하세요.']})

    # [POST] - 유저 회원가입 실패 테스트(패스워드 형식 에러:특수문자X)
    def test_fail_user_signup_due_to_password_no_special_letters(self):
        data = {
            'email': 'test01@gmail.com',
            'nickname': 'DGK01',
            'password': 'DGKtest123',
        }

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['올바른 비밀번호를 입력하세요.']})

    # [POST] - 유저 회원가입 실패 테스트(패스워드 형식 에러:허용되지 않은 특수문자)
    def test_fail_user_signup_due_to_password_unexpected_special_letters(self):
        data = {
            'email': 'test01@gmail.com',
            'nickname': 'DGK01',
            'password': 'DGKtest123!!./',
        }

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['올바른 비밀번호를 입력하세요.']})
