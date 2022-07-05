import json

from rest_framework.test import APITestCase

from users.models import User


class UserSignUpTest(APITestCase):

    maxDiff = None

    """
    setup test database
    """

    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='test-02@gmail.com', nick_name='DGK-02', hashed_password='DGK12345678')

    """
    signup success test code
    """

    def test_success_user_signup(self):
        data = {'email': 'test-01@gmail.com', 'nick_name': 'DGK-01', 'hashed_password': 'DGK12345678'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {'email': 'test-01@gmail.com', 'nick_name': 'DGK-01'})

    """
    signup fail test code
    """

    ### email test ###
    def test_fail_user_signup_due_to_email_format_validation(self):
        data = {'email': 'test-01@gmail', 'nick_name': 'DGK-01', 'hashed_password': 'DGK12345678'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'email': ['유효한 이메일 주소를 입력하십시오.']})

    def test_fail_user_signup_due_to_already_existed_email(self):
        data = {'email': 'test-02@gmail.com', 'nick_name': 'DGK-02', 'hashed_password': 'DGK12345678'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'email': ['user의 email은/는 이미 존재합니다.']})

    def test_fail_user_signup_due_to_email_required_validation(self):
        data = {'nick_name': 'DGK-01', 'hashed_password': 'DGK12345678'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'email': ['이 필드는 필수 항목입니다.']})

    ### password test ###
    def test_fail_user_signup_due_to_password_gt_20_validation(self):
        data = {'email': 'test-01@gmail.com', 'nick_name': 'DGK-01', 'hashed_password': 'DGK123456789101112131415'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'password': ['유효한 패스워드를 입력하십시오.']})

    def test_fail_user_signup_due_to_password_lt_8_validation(self):
        data = {'email': 'test-01@gmail.com', 'nick_name': 'DGK-01', 'hashed_password': 'DGK1234'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'password': ['유효한 패스워드를 입력하십시오.']})

    def test_fail_user_signup_due_to_password_required_validation(self):
        data = {'email': 'test-01@gmail.com', 'nick_name': 'DGK-01'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'hashed_password': ['이 필드는 필수 항목입니다.']})

    ### nickname test ###
    def test_fail_user_signup_due_to_nickname_required_validation(self):
        data = {'email': 'test-01@gmail.com', 'hashed_password': 'DGK12345678'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'nick_name': ['이 필드는 필수 항목입니다.']})
