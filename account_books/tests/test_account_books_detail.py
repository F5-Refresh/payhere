import json

from account_books.models import AccountBook, AccountCategory, AccountDetail
from account_books.views.account_book_detail_views import (
    AccountBookDetailAPI,
    AccountBookDetailDeleteAPI,
    AccountBookDetailListAPI,
)
from django.urls import reverse
from payhere.test_models import TestModel
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase
from users.models import User


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
        self.account_category = AccountCategory.objects.create(user=self.user, category_name='식비')

        # 가계부 내역 생성
        self.account_book_detail = AccountDetail.objects.create(
            written_date='2022-07-06T15:07:35+09:00',
            price=1500,
            description="subway",
            account_type=1,
            account_category=self.account_category,
            account_book=self.account_book,
        )

    # [성공] 가계부 내역의 전체 리스트를 조회합니다.
    def test_success_get_account_book_list(self):

        user_data = {'email': 'test2@gmail.com', 'password': 'test2@A!'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

        list_url = reverse(
            'account-book:book_detail',
            kwargs={'book_id': self.account_book.id, 'accounts_id': self.account_book_detail.id},
        )
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
            'account_category': self.account_category,
            'account_book': self.account_book,
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
        print(self.account_book.id)
        response = view(request, self.account_book.id)
        print('response', response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AccountBookDetailAPITestCase(APITestCase):

    '''
    Writer: 남효정
    Date: 2022-07-06

    각 가계부의 단일 내역을 Read, Update, Delete 합니다.
    '''

    # 초기 데이터 생성
    def setUp(self):

        # 유저 생성
        self.user = User.objects.create_user(nickname='test2', email='test2@gmail.com', password='test2@A!')

        # 가계부 생성
        self.account_book = AccountBook.objects.create(user=self.user, book_name='test', budget='10000')

        # 카테고리 생성
        self.account_category = AccountCategory.objects.create(user=self.user, category_name='식비')

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
            'account-book:book_detail',
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

        object_url = reverse('account-book:book_detail', kwargs={'book_id': 0, 'accounts_id': 0})
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

    # [성공] 가계부 내역 삭제: 가계부 id, 가계부 내역 id를 받고 해당되는 단일 내역 삭제를 테스트합니다. (delete_flag 상태만 변경됩니다.)
    def test_success_patch_a_delete_flag(self):

        user_data = {'email': 'test2@gmail.com', 'password': 'test2@A!'}
        response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
        access_token = response.data['access']
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

        object_url = 'account-books//accounts//deleted'
        data = {'written_date': '2022-07-06 05:46:57', 'price': 10000, 'account_type': 1, 'account_book': 1}

        factory = APIRequestFactory()
        request = factory.patch(object_url, data=data, format='json', **headers)
        view = AccountBookDetailDeleteAPI.as_view()
        response = view(request, self.account_book.id, self.account_book_detail.id)
        if response.data['detail'] == '레코드가 삭제되었습니다.':
            self.assertEqual(response.data['account_detail'].delete_flag, True)
        else:
            self.assertEqual(response.data['account_detail'].delete_flag, False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
        self.account_category = AccountCategory.objects.create(user=self.user, category_name='교통비')

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
