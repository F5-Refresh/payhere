from django.urls import path

from account_books.views.account_category_views import AcoountCategoryView

urlpatterns = [
    path('account_categoty', AcoountCategoryView.as_view()),
    path('account_categoty/<int:account_category_id>', AcoountCategoryView.as_view()),
]
