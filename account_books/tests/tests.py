# import json

# from account_books.models import AccountBook, AccountCategory, AccountDetail
# from account_books.views.account_category_views import AcoountCategoryView
# from payhere.test_models import LoginTestModel
# from rest_framework import status
# from rest_framework.test import APIClient, APIRequestFactory, APITestCase, force_authenticate
# from users.models import User

# class AccountCategoryTest(APITestCase):

#     '''카테고리 View 테스트

#     Writer: 이동연
#     Date: 2022-07-05

#     카테고리 View 테스트를 담당하고 있습니다.
#     '''

#     def setUp(self):
#         self.user = User.objects.create(email='test1@test.com', password='F5-refresh!', nickname='foo')
#         self.login_test = TestModel(self.user)
#         another_user = User.objects.create(email='test2@test.com', password='F5-refresh!', nickname='bar')
#         self.account_book = AccountBook.objects.create(user=self.user, book_name='일반 가계부', budget=150000)
#         AccountCategory.objects.create(category_name='test1', user=self.user)
#         AccountCategory.objects.create(category_name='test2', user=self.user)
#         AccountCategory.objects.create(category_name='test3', user=self.user)
#         AccountCategory.objects.create(category_name='test4', user=self.user)
#         AccountCategory.objects.create(category_name='test5', user=another_user)

#     # 카테고리 리스트가 정상적으로 조회되었는지 테스트합니다.
#     def test_get(self):
#         response = self.login_test.login_user_case(
#             view=AcoountCategoryView.as_view(), url='/account_category', method='get'
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         account_categorise = AccountCategory.objects.filter(user=self.user, delete_flag=False).order_by(
#             'category_name'
#         )
#         for data, account_category in zip(response.data, account_categorise):
#             self.assertEqual(data['id'], account_category.id)

#     # 카테고리가 정상적으로 생성 처리되었는지 테스트합니다.
#     def test_post(self):
#         response = self.login_test.login_user_case(
#             view=AcoountCategoryView.as_view(), url='/account_category', method='post', data={'category_name': '주거비'}
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         if not AccountCategory.objects.filter(user=self.user, category_name='주거비'):
#             self.fail('데이터가 생성되지 않았습니다.')

#     # 카테고리가 정상적으로 수정 처리되었는지 테스트합니다
#     def test_patch(self):
#         account_category = AccountCategory.objects.create(category_name='주비', user=self.user)
#         response = self.login_test.login_user_case(
#             account_category.id,
#             view=AcoountCategoryView.as_view(),
#             url='/account_category',
#             method='patch',
#             data={'category_name': '주거비'},
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         if not AccountCategory.objects.filter(id=account_category.id, user=self.user, category_name='주거비'):
#             self.fail('데이터가 갱신되지 않았습니다')

#     # 카테고리가 정상적으로 삭제/복구 처리되었는지 테스트합니다.
#     def test_toggle_delete(self):
#         account_category = AccountCategory.objects.create(category_name='식비', user=self.user)
#         response = self.login_test.login_user_case(
#             account_category.id,
#             view=AcoountCategoryView.toggle_delete,
#             url='/account_category/toggle_delet',
#             method='patch',
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         if AccountCategory.objects.filter(id=account_category.id, delete_flag=False):
#             self.fail('데이터가 삭제되지 않았습니다.')

#         response = self.login_test.login_user_case(
#             account_category.id,
#             view=AcoountCategoryView.toggle_delete,
#             url='/account_category/toggle_delet',
#             method='patch',
#         )
#         if AccountCategory.objects.filter(id=account_category.id, delete_flag=True):
#             self.fail('데이터가 복구되지 않았습니다.')


# class AccountTest(APITestCase):
#     '''
#     전기원
#     2022-07-06
#     '''

#     def setUp(self):
#         self.user = User.objects.create_user(nickname='haha', email='test1@gmail.com', password='test12345!T')

#         # self.user = User.objects.create_user(nickname='chacha', email='test2@gmail.com', password='test55555!T')
#         self.account_book = AccountBook.objects.create(user=self.user, book_name='데이트통장', budget=3000000)

#     # 가계부 리스트 조회 성공 테스트입니다.
#     def test_get_success_accountbook_list(self):
#         client = APIClient()
#         user_data = {'email': 'test1@gmail.com', 'password': 'test12345!T'}
#         response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
#         access_token = response.data['access']
#         headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
#         url = "/account-books"
#         response = self.client.get(url, **headers)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # results = [
#         #     {'book_name': '데이트통장', 'budget': '3000000', 'delete_flag': False},
#         #     {'book_name': '관리비', 'budget': '1100000', 'delete_flag': False},
#         # ]
#         # self.maxDiff = None
#         # self.assertEqual(response.json(), results)

#     # # 가계부 생성 성공 테스트입니다.
#     def test_success_create_accountbook(self):
#         client = APIClient()
#         user_data = {'email': 'test1@gmail.com', 'password': 'test12345!T'}
#         response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
#         access_token = response.data['access']
#         headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
#         url = "/account-books"
#         response = self.client.get(url, **headers)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         data = {
#             'user': self.user.id,
#             'book_name': '생활비',
#             'budget': 2000000,
#         }
#         url = "/account-books"
#         res = json.dumps(data)
#         response = client.post(url, res, content_type='application/json', **headers)
#         self.maxDiff = None
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     # # 가계부 수정 성공 테스트 입니다.
#     def test_success_update_accountbook(self):
#         client = APIClient()
#         user_data = {'email': 'test1@gmail.com', 'password': 'test12345!T'}
#         response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
#         access_token = response.data['access']
#         headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
#         url = "/account-books"
#         response = self.client.get(url, **headers)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         data = AccountBook.objects.create(user=self.user, book_name='데이트통장', budget=2222222)
#         url = f'/account-books/{data.id}'

#         # book_id = AccountBook.objects.filter(id=data.id)
#         # print(book_id)
#         revised_data = {'user': self.user.id, 'book_name': '수정 데이트통장', 'budget': 333333}
#         res = json.dumps(revised_data)
#         response = client.patch(url, res, content_type='application/json', **headers)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     # user가 없어 가계부 수정이 불가능한 실패테스트입니다.
#     def test_fail_update_accountbook_due_to_id_not_existed(self):
#         client = APIClient()
#         user_data = {'email': 'test1@gmail.com', 'password': 'test12345!T'}
#         response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
#         access_token = response.data['access']
#         headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
#         url = "/account-books"
#         response = self.client.get(url, **headers)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         data = AccountBook.objects.create(user=self.user, book_name='데이트 실패 통장', budget=2222222)
#         url = f'/account-books/{data.id}'
#         revised_data = {'user': 4, 'book_name': '수정 데이트통장', 'budget': 333333}
#         res = json.dumps(revised_data)
#         response = client.patch(url, res, content_type='application/json', **headers)
#         print(response.json())
#         self.maxDiff = None
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     # # 가계부 삭제리스트를 조회하는 성공 테스트입니다.
#     def test_get_deleted_list(self):
#         client = APIClient()
#         user_data = {'email': 'test1@gmail.com', 'password': 'test12345!T'}
#         response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
#         access_token = response.data['access']
#         headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
#         url = "/account-books"
#         response = self.client.get(url, **headers)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         client = APIClient()
#         url = "/account-books/deleted_list"
#         response = client.get(url, content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         print(response.json())

#     # 가계부를 삭제하는 것을 성공하는 테스트입니다.
#     def test_get_deleted(self):
#         client = APIClient()
#         user_data = {'email': 'test1@gmail.com', 'password': 'test12345!T'}
#         response = self.client.post('/users/signin', data=json.dumps(user_data), content_type='application/json')
#         access_token = response.data['access']
#         headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
#         url = "/account-books"
#         response = self.client.get(url, **headers)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         data = AccountBook.objects.create(user=self.user, book_name='데이트통장', budget=55555)
#         # data.toggle_active()  # True
#         url = f'/account-books/toggle_delete/{data.id}'
#         # res = json.dumps(**data)
#         response = client.patch(url, **headers)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         print(response.json())
