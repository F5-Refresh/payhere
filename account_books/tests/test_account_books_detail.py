import json

from account_books.models import AccountBook, AccountCategory, AccountDetail
from account_books.views.account_book_detail_views import AccountBookDetailView
from django.urls import reverse
from payhere.test_models import LoginTestModel
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase
from users.models import User


class AccountBookDetailTestCase(APITestCase):

    '''
    Writer: 남효정
    Date: 2022-07-06

    '''

    # 초기 데이터 생성
    def setUp(self):

        # 유저 생성
        self.user = User.objects.create_user(nickname='test2', email='test2@gmail.com', password='test2@A!')
        self.login_test = LoginTestModel(self.user)

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

        url = '/account-books//accounts'
        response = self.login_test.login_user_case(
            self.account_book.id, view=AccountBookDetailView.as_view(), url=url, method='get'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # [성공] 가계부 내역에서 1개의 내역을 생성합니다.
    def test_success_post_account_book_object(self):

        data = {
            'written_date': '2022-07-06T15:07:35+09:00',
            'price': 1500,
            'account_type': 1,
            'account_category': self.account_category.id,
            'account_book': self.account_book.id,
        }

        url = '/account-books//accounts'
        response = self.login_test.login_user_case(
            self.account_book.id, view=AccountBookDetailView.as_view(), url=url, method='post', data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # [실패] 가계부 내역에서 1개의 내역을 생성합니다. / 빈 data를 보내서 테스트합니다.
    def test_fail_post_account_book_object(self):

        data = {}
        url = '/account-books//accounts'
        response = self.login_test.login_user_case(
            self.account_book.id, view=AccountBookDetailView.as_view(), url=url, method='post', data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # [성공] 가계부 내역 수정: 가계부 id, 가계부 내역 id를 받고 해당되는 단일 내역 수정을 테스트합니다.
    def test_success_patch_a_account_book_object(self):

        data = {
            'written_date': '2022-07-06T15:07:35+09:00',
            'price': 50000,
            'description': "train",
            'account_type': 1,
            'account_category': self.account_category.id,
            'account_book': self.account_book.id,
        }

        url = 'account-books//accounts/detail/'
        response = self.login_test.login_user_case(
            self.account_book.id,
            self.account_book_detail.id,
            view=AccountBookDetailView.as_view(),
            url=url,
            method='patch',
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # [실패] 가계부 내역 수정: 가계부 id, 가계부 내역 id를 받고 해당되는 단일 내역 수정을 테스트합니다. / 빈 데이터를 보내서 테스트 합니다.
    def test_fail_patch_a_account_book_object(self):

        data = {}
        url = 'account-books//accounts/detail/'
        response = self.login_test.login_user_case(
            self.account_book.id,
            self.account_book_detail.id,
            view=AccountBookDetailView.as_view(),
            url=url,
            method='patch',
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # [성공] 가계부 내역 상세조회: 가계부 id, 가계부 내역 id를 받고 해당되는 단일 내역을 테스트합니다.
    def test_success_get_a_account_book_object(self):

        url = 'account-books//accounts/detail/'
        response = self.login_test.login_user_case(
            self.account_book.id,
            self.account_book_detail.id,
            view=AccountBookDetailView.detail,
            url=url,
            method='get',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # [실패] 가계부 내역 상세조회: 가계부 id, 가계부 내역 id를 받고 해당되는 단일 내역을 테스트합니다. / 존재하지 않는 book_id, accounts_id로 테스트합니다.
    def test_fail_get_a_account_book_object(self):

        url = 'account-books//accounts/detail/'
        response = self.login_test.login_user_case(0, 0, view=AccountBookDetailView.detail, url=url, method='get')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # [성공] 가계부 내역 삭제: 가계부 id, 가계부 내역 id를 받고 해당되는 단일 내역 삭제를 테스트합니다. (delete_flag 상태만 변경됩니다.)
    def test_success_patch_a_delete_flag(self):

        url = 'account-books//accounts//deleted'

        # 한번에 삭제, 복구 둘 다 테스트하게 됩니다.
        # (1) 삭제 혹은 복구를 테스트합니다.
        response = self.login_test.login_user_case(
            self.account_book.id,
            self.account_book_detail.id,
            view=AccountBookDetailView.toggle_active,
            url=url,
            method='patch',
        )

        self.account_book_detail.refresh_from_db()

        self.assertEqual(self.account_book_detail.delete_flag, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # (1) 위에서 했던 테스트의 반대 행동을 테스트 합니다.
        response = self.login_test.login_user_case(
            self.account_book.id,
            self.account_book_detail.id,
            view=AccountBookDetailView.toggle_active,
            url=url,
            method='patch',
        )

        self.account_book_detail.refresh_from_db()

        self.assertEqual(self.account_book_detail.delete_flag, False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
