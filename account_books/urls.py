from django.urls import path

from account_books.views import AccountBookList, AccountBookView
from account_books.views.account_category_views import AcoountCategoryView

urlpatterns = [
    path('account_category', AcoountCategoryView.as_view()),
    path('account_category/<int:account_category_id>', AcoountCategoryView.as_view()),
    path('account_category/toggle_delete/<int:account_category_id>', AcoountCategoryView.toggle_delete),
    path('account-books', AccountBookList.as_view()),
    path('account-books/<int:book_id>', AccountBookView.as_view()),
    path('account-books/deleted', AccountBookView.deleted_list),
]

