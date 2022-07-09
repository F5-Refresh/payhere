import json

from account_books.models import AccountBook, AccountCategory, AccountDetail
from account_books.views.account_book_views import AccountBookView
from payhere.test_models import LoginTestModel
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from users.models import User


class AccountTest(APITestCase):
    '''가계부 View 테스트

    writer : 전기원
    date : 2022-07-05

    가계부의 CRUD 를 테스트합니다.
    '''

    def setUp(self):
        self.user = User.objects.create_user(nickname='haha', email='test1@gmail.com', password='test12345!T')
        self.login_test = LoginTestModel(self.user)

        self.account_book = AccountBook.objects.create(user=self.user, book_name='데이트통장', budget=3000000)
        AccountBook.objects.create(user=self.user, book_name='데이트통장', budget=4440000, delete_flag=True)
        AccountBook.objects.create(user=self.user, book_name='생활비통장', budget=5500000)
        AccountBook.objects.create(user=self.user, book_name='관리비통장', budget=2000000)

    # 가계부 리스트 조회 성공 테스트입니다.
    def test_get_success_accountbook_list(self):
        response = self.login_test.login_user_case(view=AccountBookView.as_view(), url='/account-books', method='get')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.login_test.login_user_case(
            view=AccountBookView.as_view(), url='/account-books', method='get', data={'deleted': True}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        account_books = self.user.account_books.filter(delete_flag=True)
        for data, book in zip(response.data, account_books):
            self.assertEqual(data['book_name'], book.book_name)

    # 가계부 생성 성공 테스트입니다.
    def test_success_create_accountbook(self):

        data = {
            'user': self.user.id,
            'book_name': '생활비',
            'budget': 2000000,
        }

        response = self.login_test.login_user_case(
            view=AccountBookView.as_view(), url='/account-books', method='post', data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # 가계부 수정 성공 테스트 입니다.
    def test_success_update_accountbook(self):
        client = APIClient()
        data = AccountBook.objects.create(user=self.user, book_name='데이트통장', budget=2222222)
        url = f'/account-books/{data.id}'
        revised_data = {'user': self.user.id, 'book_name': '수정 데이트통장', 'budget': 333333}

        response = self.login_test.login_user_case(
            data.id, view=AccountBookView.as_view(), url=url, method='patch', data=revised_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 가계부를 삭제하는 것을 성공하는 테스트입니다.
    def test_get_deleted(self):
        data = AccountBook.objects.create(user=self.user, book_name='데이트통장', budget=55555)
        url = f'/account-books/toggle_delete/{data.id}'
        response = self.login_test.login_user_case(
            data.id, view=AccountBookView.toggle_active, url=url, method='patch'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
