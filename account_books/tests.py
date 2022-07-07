import json

from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase, force_authenticate
from users.models import User

from account_books.models import AccountBook, AccountCategory, AccountDetail
from account_books.views.account_category_views import AcoountCategoryView


class AccountCategoryTest(APITestCase):

    '''
    이동연
    2022-07-06
    '''

    def setUp(self):
        self.user = User.objects.create(email='test1@test.com', password='F5-refresh!', nickname='foo')
        another_user = User.objects.create(email='test2@test.com', password='F5-refresh!', nickname='bar')
        self.account_book = AccountBook.objects.create(user=self.user, book_name='일반 가계부', budget=150000)
        AccountCategory.objects.create(category_name='test1', user=self.user)
        AccountCategory.objects.create(category_name='test2', user=self.user)
        AccountCategory.objects.create(category_name='test3', user=self.user)
        AccountCategory.objects.create(category_name='test4', user=self.user)
        AccountCategory.objects.create(category_name='test5', user=another_user)

    # Note: 로그인에 대한 테스트 코드가 필요할까? 코드 리팩토링 후 삭제 예정

    # def test_login_get(self):
    #     factory = APIRequestFactory()
    #     request = factory.get('/account_category')
    #     view = AcoountCategoryView.as_view()
    #     force_authenticate(request, user=self.user)
    #     response = view(request)
    #     if response.data[0].get('id', None) == None:
    #         self.fail()

    # def test_not_login_get(self):
    #     factory = APIRequestFactory()
    #     request = factory.get('/account_category')
    #     view = AcoountCategoryView.as_view()
    #     try:
    #         view(request)
    #         self.fail()
    #     except:
    #         pass

    def test_get(self):
        factory = APIRequestFactory()
        request = factory.get('/account_category')
        view = AcoountCategoryView.as_view()
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        account_categorise = AccountCategory.objects.filter(user=self.user, delete_flag=False).order_by(
            'category_name'
        )
        # 데이터 확인 테스트
        for data, account_category in zip(response.data, account_categorise):
            self.assertEqual(data['id'], account_category.id)

    def test_post(self):
        factory = APIRequestFactory()
        request = factory.post('/account_category', data={'category_name': '주거비'})
        view = AcoountCategoryView.as_view()
        force_authenticate(request, user=self.user)
        response = view(request)
        # 데이터 생성 확인 테스트
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        if not AccountCategory.objects.filter(user=self.user, category_name='주거비'):
            self.fail('데이터가 생성되지 않았습니다.')

    def test_patch(self):
        account_category = AccountCategory.objects.create(category_name='주비', user=self.user)
        factory = APIRequestFactory()
        request = factory.patch('/account_category', data={'category_name': '주거비'})
        view = AcoountCategoryView.as_view()
        force_authenticate(request, user=self.user)
        response = view(request, account_category.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 데이터 갱신 확인 테스트
        if not AccountCategory.objects.filter(id=account_category.id, user=self.user, category_name='주거비'):
            self.fail('데이터가 갱신되지 않았습니다')

    def test_toggle_delete(self):
        account_category = AccountCategory.objects.create(category_name='식비', user=self.user)
        factory = APIRequestFactory()
        request = factory.patch('/account_category/toggle_delete')
        view = AcoountCategoryView.toggle_delete
        force_authenticate(request, user=self.user)
        response = view(request, account_category.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 데이터 삭제 확인 테스트
        if AccountCategory.objects.filter(id=account_category.id, delete_flag=False):
            self.fail('데이터가 삭제되지 않았습니다.')
        response = view(request, account_category.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AccountTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        client = APIClient()
        user1 = User.objects.create(id=1, email='testuser1@gmail.com', password='kiwon12345~', nickname='testtest')
        user2 = User.objects.create(id=2, email='testuser2@gmail.com', password='kiwon11111~', nickname='chachacha')

        AccountBook.objects.create(id=1, user_id=1, book_name='데이트통장', budget=3000000)
        AccountBook.objects.create(id=2, user_id=1, book_name='관리비', budget=1000000)

        client.force_authenticate(user1)
        client.force_authenticate(user2)

    # 가계부 리스트 조회 성공 테스트입니다.
    def test_get_success_accountbook_list(self):
        client = APIClient()
        url = "/account-books"
        response = client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.json())
        results = [
            {'book_name': '데이트통장', 'budget': '3000000', 'delete_flag': False},
            {'book_name': '관리비', 'budget': '1000000', 'delete_flag': False},
        ]
        self.maxDiff = None
        self.assertEqual(response.json(), results)

    # 가계부 생성 성공 테스트입니다.
    def test_success_create_accountbook(self):
        client = APIClient()
        data = {
            'user': 1,
            'book_name': '생활비',
            'budget': 2000000,
        }
        url = "/account-books"
        res = json.dumps(data)

        response = client.post(url, res, content_type='application/json')
        print(response.json())
        self.maxDiff = None
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # 가계부 수정 성공 테스트 입니다.
    def test_success_update_accountbook(self):
        client = APIClient()
        data = {'user': 1, 'book_name': '수정 데이트통장', 'budget': 2222222}
        url = "/account-books/1"
        res = json.dumps(data)
        response = client.patch(url, res, content_type='application/json')
        print(response.json())
        self.maxDiff = None
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # user가 없어 가계부 수정이 불가능한 실패테스트입니다.
    def test_fail_update_accountbook_due_to_id_not_existed(self):
        client = APIClient()
        data = {'user': 3, 'book_name': '수정 실패 데이트통장', 'budget': 223222}
        url = "/account-books/1"
        res = json.dumps(data)
        response = client.patch(url, res, content_type='application/json')
        print(response.json())
        self.maxDiff = None
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 가계부가 없어 수정이 불가능한 실패 테스트입니다.
    def test_fail_update_accountbook_due_to_accountbook_not_exist(self):
        client = APIClient()
        data = {'user': 1, 'book_name': '실패 데이트통장', 'budget': 333333}
        url = "/account-books/4"
        res = json.dumps(data)
        response = client.patch(url, res, content_type='application/json')
        print(response.json())
        self.maxDiff = None
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # 가계부 삭제리스트를 조회하는 성공 테스트입니다.
    def test_get_deleted_list(self):
        client = APIClient()
        url = "/account-books/deleted"
        response = client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.json())
