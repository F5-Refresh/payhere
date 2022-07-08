import json

from django.urls import reverse
from payhere.test_models import TestModel
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase, force_authenticate
from users.models import User

from account_books.models import AccountBook, AccountCategory, AccountDetail
from account_books.views.account_book_detail import AccountBookDetailAPI
from account_books.views.account_book_detail_list import AccountBookDetailListAPI
from account_books.views.account_category_views import AcoountCategoryView


class AccountCategoryTest(APITestCase):

    '''
    이동연
    2022-07-06
    '''

    def setUp(self):
        self.user = User.objects.create(email='test1@test.com', password='F5-refresh!', nickname='foo')
        self.login_test = TestModel(self.user)
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
        response = self.login_test.login_user_case(
            view=AcoountCategoryView.as_view(), url='/account_category', method='get'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        account_categorise = AccountCategory.objects.filter(user=self.user, delete_flag=False).order_by(
            'category_name'
        )
        # 데이터 확인 테스트
        for data, account_category in zip(response.data, account_categorise):
            self.assertEqual(data['id'], account_category.id)

    def test_post(self):
        response = self.login_test.login_user_case(
            view=AcoountCategoryView.as_view(), url='/account_category', method='post', data={'category_name': '주거비'}
        )
        # 데이터 생성 확인 테스트
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        if not AccountCategory.objects.filter(user=self.user, category_name='주거비'):
            self.fail('데이터가 생성되지 않았습니다.')

    def test_patch(self):
        account_category = AccountCategory.objects.create(category_name='주비', user=self.user)
        response = self.login_test.login_user_case(
            account_category.id,
            view=AcoountCategoryView.as_view(),
            url='/account_category',
            method='patch',
            data={'category_name': '주거비'},
        )
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

        response = self.login_test.login_user_case(
            account_category.id,
            view=AcoountCategoryView.toggle_delete,
            url='/account_category/toggle_delet',
            method='patch',
        )
        if AccountCategory.objects.filter(id=account_category.id, delete_flag=True):
            self.fail('데이터가 복구되지 않았습니다.')


class AccountTest(APITestCase):
    '''
    전기원
    2022-07-06
    '''

    def setUp(self):
        self.user = User.objects.create_user(nickname='haha', email='test1@gmail.com', password='test12345!T')

        # self.user = User.objects.create_user(nickname='chacha', email='test2@gmail.com', password='test55555!T')
        self.account_book = AccountBook.objects.create(user=self.user, book_name='데이트통장', budget=3000000)

    # 가계부 리스트 조회 성공 테스트입니다.
    def test_get_success_accountbook_list(self):
        client = APIClient()
        user_data = {'email': 'test1@gmail.com', 'password': 'test12345!T'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        url = "/account-books"
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # results = [
        #     {'book_name': '데이트통장', 'budget': '3000000', 'delete_flag': False},
        #     {'book_name': '관리비', 'budget': '1100000', 'delete_flag': False},
        # ]
        # self.maxDiff = None
        # self.assertEqual(response.json(), results)

    # # 가계부 생성 성공 테스트입니다.
    def test_success_create_accountbook(self):
        client = APIClient()
        user_data = {'email': 'test1@gmail.com', 'password': 'test12345!T'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        url = "/account-books"
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            'user': self.user.id,
            'book_name': '생활비',
            'budget': 2000000,
        }
        url = "/account-books"
        res = json.dumps(data)
        response = client.post(url, res, content_type='application/json', **headers)
        self.maxDiff = None
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # # 가계부 수정 성공 테스트 입니다.
    def test_success_update_accountbook(self):
        client = APIClient()
        user_data = {'email': 'test1@gmail.com', 'password': 'test12345!T'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        url = "/account-books"
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = AccountBook.objects.create(user=self.user, book_name='데이트통장', budget=2222222)
        url = f'/account-books/{data.id}'

        # book_id = AccountBook.objects.filter(id=data.id)
        # print(book_id)
        revised_data = {'user': self.user.id, 'book_name': '수정 데이트통장', 'budget': 333333}
        res = json.dumps(revised_data)
        response = client.patch(url, res, content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # user가 없어 가계부 수정이 불가능한 실패테스트입니다.
    def test_fail_update_accountbook_due_to_id_not_existed(self):
        client = APIClient()
        user_data = {'email': 'test1@gmail.com', 'password': 'test12345!T'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        url = "/account-books"
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = AccountBook.objects.create(user=self.user, book_name='데이트 실패 통장', budget=2222222)
        url = f'/account-books/{data.id}'
        revised_data = {'user': 4, 'book_name': '수정 데이트통장', 'budget': 333333}
        res = json.dumps(revised_data)
        response = client.patch(url, res, content_type='application/json', **headers)
        print(response.json())
        self.maxDiff = None
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # # 가계부 삭제리스트를 조회하는 성공 테스트입니다.
    def test_get_deleted_list(self):
        client = APIClient()
        user_data = {'email': 'test1@gmail.com', 'password': 'test12345!T'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        url = "/account-books"
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        client = APIClient()
        url = "/account-books/deleted_list"
        response = client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.json())

    # 가계부를 삭제하는 것을 성공하는 테스트입니다.
    def test_get_deleted(self):
        client = APIClient()
        user_data = {'email': 'test1@gmail.com', 'password': 'test12345!T'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        url = "/account-books"
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = AccountBook.objects.create(user=self.user, book_name='데이트통장', budget=55555)
        # data.toggle_active()  # True
        url = f'/account-books/toggle_delete/{data.id}'
        # res = json.dumps(**data)
        response = client.patch(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.json())

        response = view(request, account_category.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AccountBookDetailListAPITestCase(APITestCase):

    '''
    Writer: 남효정
    Date: 2022-07-06

    각 가계부 내역의 Create, Read(List)를 테스트합니다.
    '''

    # 초기 데이터 생성
    def setUp(self):

        # 유저 생성
        self.user = User.objects.create_user(nickname='test2', email='test2@gmail.com', password='test2@A!')

        # 가계부 생성
        self.account_book = AccountBook.objects.create(
            user=self.user, book_name='test', budget='10000', delete_flag=False
        )

        # 카테고리 생성
        self.account_category = AccountCategory.objects.create(category_name='식비')

    # [성공] 가계부 내역의 전체 리스트를 조회합니다.
    def test_success_get_account_book_list(self):

        user_data = {'email': 'test2@gmail.com', 'password': 'test2@A!'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

        list_url = reverse('account-book:book-details', kwargs={'book_id': self.account_book.id})
        response = self.client.get(list_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # [성공] 가계부 내역에서 1개의 내역을 생성합니다.
    def test_success_post_account_book_object(self):

        user_data = {'email': 'test2@gmail.com', 'password': 'test2@A!'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

        list_url = 'account-books//accounts'

        data = {
            'written_date': '2022-07-06T15:07:35+09:00',
            'price': 1500,
            'description': "subway",
            'account_type': 1,
            'account_category': self.account_category.id,
            'account_book': self.account_book.id,
        }

        factory = APIRequestFactory()
        request = factory.post(list_url, data=data, format='json', **headers)
        view = AccountBookDetailListAPI.as_view()
        response = view(request, self.account_book.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # [실패] 가계부 내역에서 1개의 내역을 생성합니다. / 빈 data를 보내서 테스트합니다.
    def test_fail_post_account_book_object(self):

        list_url = 'account-books//accounts'

        data = {}

        user_data = {'email': 'test2@gmail.com', 'password': 'test2@A!'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

        factory = APIRequestFactory()
        request = factory.post(list_url, data=data, format='json', **headers)
        view = AccountBookDetailListAPI.as_view()
        response = view(request, self.account_book.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AccountBookDetailAPITestCase(APITestCase):

    '''
    Writer: 남효정
    Date: 2022-07-06

    각 가계부의 단일 내역을 Read, Update 합니다.
    '''

    # 초기 데이터 생성
    def setUp(self):

        # 유저 생성
        self.user = User.objects.create_user(nickname='test2', email='test2@gmail.com', password='test2@A!')

        # 가계부 생성
        self.account_book = AccountBook.objects.create(user=self.user, book_name='test', budget='10000')

        # 카테고리 생성
        self.account_category = AccountCategory.objects.create(category_name='식비')

        # 가계부 내역 생성
        self.account_book_detail = AccountDetail.objects.create(
            written_date='2022-07-06T15:07:35+09:00',
            price=1500,
            description="subway",
            account_type=1,
            account_category=self.account_category,
            account_book=self.account_book,
        )

    # [성공] 가계부 내역 상세조회: 가계부 id, 가계부 내역 id를 받고 해당되는 단일 내역을 테스트합니다.
    def test_success_get_a_account_book_object(self):

        user_data = {'email': 'test2@gmail.com', 'password': 'test2@A!'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

        object_url = reverse(
            'account-book:book-detail',
            kwargs={'book_id': self.account_book.id, 'accounts_id': self.account_book_detail.id},
        )
        response = self.client.get(object_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # [실패] 가계부 내역 상세조회: 가계부 id, 가계부 내역 id를 받고 해당되는 단일 내역을 테스트합니다. / 존재하지 않는 book_id, accounts_id로 테스트합니다.
    def test_fail_get_a_account_book_object(self):

        user_data = {'email': 'test2@gmail.com', 'password': 'test2@A!'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

        object_url = reverse('account-book:book-detail', kwargs={'book_id': 0, 'accounts_id': 0})
        response = self.client.get(object_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # [성공] 가계부 내역 수정: 가계부 id, 가계부 내역 id를 받고 해당되는 단일 내역 수정을 테스트합니다.
    def test_success_patch_a_account_book_object(self):

        user_data = {'email': 'test2@gmail.com', 'password': 'test2@A!'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

        object_url = 'account-books//accounts/'

        data = {
            'written_date': '2022-07-06T15:07:35+09:00',
            'price': 50000,
            'description': "train",
            'account_type': 1,
            'account_category': self.account_category.id,
            'account_book': self.account_book.id,
        }

        factory = APIRequestFactory()
        request = factory.patch(object_url, data=data, format='json', **headers)
        view = AccountBookDetailAPI.as_view()
        response = view(request, self.account_book.id, self.account_book_detail.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # [실패] 가계부 내역 수정: 가계부 id, 가계부 내역 id를 받고 해당되는 단일 내역 수정을 테스트합니다. / 빈 데이터를 보내서 테스트 합니다.
    def test_fail_patch_a_account_book_object(self):

        user_data = {'email': 'test2@gmail.com', 'password': 'test2@A!'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

        object_url = 'account-books//accounts/'

        data = {}

        factory = APIRequestFactory()
        request = factory.patch(object_url, data=data, format='json', **headers)
        view = AccountBookDetailAPI.as_view()
        response = view(request, self.account_book.id, self.account_book_detail.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AccountBookDetailListDeletedAPITestCase(APITestCase):

    '''
    Writer: 남효정
    Date: 2022-07-06

    각 가계부 내역의 삭제내역 리스트 Read(List)를 구현합니다.
    '''

    # 초기 데이터 생성
    def setUp(self):

        # 유저 생성
        self.user = User.objects.create_user(nickname='test2', email='test2@gmail.com', password='test2@A!')

        # 가계부 생성
        self.account_book = AccountBook.objects.create(user=self.user, book_name='test', budget='10000')

        # 카테고리 생성
        self.account_category = AccountCategory.objects.create(category_name='교통비')

        # 가계부 내역 생성(1): 삭제 O
        self.account_book_detail = AccountDetail.objects.create(
            written_date='2022-07-06T15:07:35+09:00',
            price=1500,
            description="subway",
            account_type=1,
            account_category=self.account_category,
            account_book=self.account_book,
            delete_flag=True,
        )

        # 가계부 내역 생성(2): 삭제 X
        self.account_book_detail = AccountDetail.objects.create(
            written_date='2022-07-06T15:07:35+09:00',
            price=2000000,
            description="airplane",
            account_type=1,
            account_category=self.account_category,
            account_book=self.account_book,
            delete_flag=False,
        )

    # [성공] 가계부 내역에서 삭제된 리스트 조회를 테스트합니다.
    def test_success_get_deleted_account_book_lists(self):

        user_data = {'email': 'test2@gmail.com', 'password': 'test2@A!'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

        list_url = reverse('account-book:book_details_deleted', kwargs={'book_id': self.account_book.id})
        response = self.client.get(list_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
