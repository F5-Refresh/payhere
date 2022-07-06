from datetime import datetime
from unicodedata import category
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from account_books.models import AccountBook, AccountCategory, AccountDetail
from account_books.views.account_category_views import AcoountCategoryView
from rest_framework import status

from users.models import User
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
        
    # Note: 로그인에 대한 테스트 코드가 필요할까?
     
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
        account_categorise= AccountCategory.objects.filter(user=self.user).order_by('category_name')
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
            self.fail()

    def test_patch(self):
        account_category = AccountCategory.objects.create(category_name='주비', user=self.user)
        factory = APIRequestFactory()
        request = factory.patch('/account_category', data={'category_name': '주거비'})
        view = AcoountCategoryView.as_view()
        force_authenticate(request, user=self.user)
        response = view(request, account_category.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 데이터 갱신 확인 테스트
        if not AccountCategory.objects.filter(id=account_category.id, user=self.user, category_name= '주거비'):
            self.fail()
    
    def test_delete(self):
        account_category = AccountCategory.objects.create(category_name='식비', user=self.user)
        factory = APIRequestFactory()
        request = factory.delete('/account_category')
        view = AcoountCategoryView.as_view()
        force_authenticate(request, user=self.user)
        response = view(request, account_category.id)
        # 데이터 삭제 확인 테스트
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 데이터 삭제 확인 테스트
        if AccountCategory.objects.filter(id=account_category.id):
            self.fail()
    

    def test_delete_fail_case(self):
        # 카테고리를 참조하는 account_detail 레코드가 있을 경우 삭제불가
        account_category = AccountCategory.objects.create(category_name='식비', user=self.user)
        AccountDetail.objects.create(
                                        written_date=datetime.now(), 
                                        account_book=self.account_book, 
                                        price=1000, 
                                        description='친구랑 밥먹음', 
                                        account_type='1',
                                        account_category=account_category,
                                    )

        factory = APIRequestFactory()
        request = factory.delete('/account_category')
        view = AcoountCategoryView.as_view()
        force_authenticate(request, user=self.user)
        response = view(request, account_category.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # 데이터 삭제 확인 테스트
        if not AccountCategory.objects.filter(id=account_category.id):
            self.fail()