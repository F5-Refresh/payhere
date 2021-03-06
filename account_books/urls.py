from django.urls import path

from account_books.views.account_book_views import AccountBookView
from account_books.views.account_category_views import AcoountCategoryView

from .views.account_book_detail_views import AccountBookDetailView

app_name = 'account-book'


urlpatterns = [
    path('account_category', AcoountCategoryView.as_view()),
    path('account_category/<int:account_category_id>', AcoountCategoryView.as_view()),
    path('account_category/toggle_active/<int:account_category_id>', AcoountCategoryView.toggle_active),
    path('account-books', AccountBookView.as_view()),
    path('account-books/<int:book_id>', AccountBookView.as_view()),
    path('account-books/toggle_delete/<int:book_id>', AccountBookView.toggle_active),
    path('account-books/<int:book_id>/accounts', AccountBookDetailView.as_view(), name='book_details'),
    path(
        'account-books/<int:book_id>/accounts/<int:accounts_id>', AccountBookDetailView.as_view(), name='book_details'
    ),
    path(
        'account-books/<int:book_id>/accounts/detail/<int:accounts_id>',
        AccountBookDetailView.detail,
        name='book_detail',
    ),
    path(
        'account-books/<int:book_id>/accounts/<int:accounts_id>/toggle_active',
        AccountBookDetailView.toggle_active,
        name='book_details_deleted',
    ),
]
