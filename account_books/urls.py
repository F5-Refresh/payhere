from django.urls import path

from account_books.views.account_book_views import AccountBookView
from account_books.views.account_category_views import AcoountCategoryView

from .views.account_book_detail import (AccountBookDetailAPI,
                                        AccountBookDetailDeleteAPI,
                                        AccountBookDetailListAPI,
                                        AccountBookDetailListDeletedAPI)

app_name = 'account-book'


urlpatterns = [
    path('account_category', AcoountCategoryView.as_view()),
    path('account_category/<int:account_category_id>', AcoountCategoryView.as_view()),
    path('account_category/toggle_active/<int:account_category_id>', AcoountCategoryView.toggle_active),
    path('account-books', AccountBookView.as_view()),
    path('account-books/<int:book_id>', AccountBookView.as_view()),
    path('account-books/toggle_delete/<int:book_id>', AccountBookView.toggle_active),
    path('account-books/deleted_list', AccountBookView.deleted_list),
    path('account-books/toggle_delete/<int:book_id>', AccountBookView.deleted_patch),
    path('account-books/<int:book_id>/accounts', AccountBookDetailListAPI.as_view(), name='books_details'),
    path('account-books/<int:book_id>/accounts/deleted_list', AccountBookDetailListDeletedAPI.as_view(), name='book_details_deleted',),
    path('account-books/<int:book_id>/accounts/<int:accounts_id>', AccountBookDetailAPI.as_view(), name='book_detail'),
    path('account-books/<int:book_id>/accounts/<int:accounts_id>/togle_delete', AccountBookDetailDeleteAPI.as_view(), name='book_detail_deleted',),
]
