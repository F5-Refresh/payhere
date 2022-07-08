from account_books.models import AccountBook, AccountCategory
from account_books.views.account_category_views import AcoountCategoryView
from payhere.test_models import LoginTestModel
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class AccountCategoryTest(APITestCase):

    '''카테고리 View 테스트

    Writer: 이동연
    Date: 2022-07-05

    카테고리 View 테스트를 담당하고 있습니다.
    '''

    def setUp(self):
        self.user = User.objects.create(email='test1@test.com', password='F5-refresh!', nickname='foo')
        self.login_test = LoginTestModel(self.user)
        another_user = User.objects.create(email='test2@test.com', password='F5-refresh!', nickname='bar')
        self.account_book = AccountBook.objects.create(user=self.user, book_name='일반 가계부', budget=150000)
        AccountCategory.objects.create(category_name='test1', user=self.user)
        AccountCategory.objects.create(category_name='test2', user=self.user)
        AccountCategory.objects.create(category_name='test3', user=self.user)
        AccountCategory.objects.create(category_name='test4', user=self.user)
        AccountCategory.objects.create(category_name='test5', user=another_user)

    # 카테고리 리스트가 정상적으로 조회되었는지 테스트합니다.
    def test_get(self):
        response = self.login_test.login_user_case(
            view=AcoountCategoryView.as_view(), url='/account_category', method='get'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        account_categorise = AccountCategory.objects.filter(user=self.user, delete_flag=False).order_by(
            'category_name'
        )
        for data, account_category in zip(response.data, account_categorise):
            self.assertEqual(data['id'], account_category.id)

    # 카테고리가 정상적으로 생성 처리되었는지 테스트합니다.
    def test_post(self):
        response = self.login_test.login_user_case(
            view=AcoountCategoryView.as_view(), url='/account_category', method='post', data={'category_name': '주거비'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        if not AccountCategory.objects.filter(user=self.user, category_name='주거비'):
            self.fail('데이터가 생성되지 않았습니다.')

    # 카테고리가 정상적으로 수정 처리되었는지 테스트합니다
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
        if not AccountCategory.objects.filter(id=account_category.id, user=self.user, category_name='주거비'):
            self.fail('데이터가 갱신되지 않았습니다')

    # 카테고리가 정상적으로 삭제/복구 처리되었는지 테스트합니다.
    def test_toggle_active(self):
        account_category = AccountCategory.objects.create(category_name='식비', user=self.user)
        response = self.login_test.login_user_case(
            account_category.id,
            view=AcoountCategoryView.toggle_active,
            url='/account_category/toggle_active',
            method='patch',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if AccountCategory.objects.filter(id=account_category.id, delete_flag=False):
            self.fail('데이터가 삭제되지 않았습니다.')

        response = self.login_test.login_user_case(
            account_category.id,
            view=AcoountCategoryView.toggle_active,
            url='/account_category/toggle_active',
            method='patch',
        )
        if AccountCategory.objects.filter(id=account_category.id, delete_flag=True):
            self.fail('데이터가 복구되지 않았습니다.')
