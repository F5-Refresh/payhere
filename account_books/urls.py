from django.urls import path

from account_books.views.account_book_views import AccountBookView
from account_books.views.account_category_views import AcoountCategoryView

urlpatterns = [
    path('account_category', AcoountCategoryView.as_view()),
    path('account_category/<int:account_category_id>', AcoountCategoryView.as_view()),
    path('account_category/toggle_active/<int:account_category_id>', AcoountCategoryView.toggle_active),
    path('account-books', AccountBookView.as_view()),
    path('account-books/<int:book_id>', AccountBookView.as_view()),
    path('account-books/toggle_delete/<int:book_id>', AccountBookView.toggle_active),
]
