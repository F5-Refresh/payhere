from core.models import TimeStamp as TimeStampModel
from django.db import models
from core.util import DeleteFlag


# 가계부
class AccountBook(TimeStampModel):
    user = models.ForeignKey('users.User', related_name='account_books', verbose_name='유저', on_delete=models.CASCADE)
    book_name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=9, decimal_places=0) # 수입, 지출 구분
    delete_flag = models.BooleanField(default=False)

    class Meta:
        db_table = 'account_books'
        
    def __str__(self):
        return f'user: {self.user.email} / book_name: {self.book_name}'
     


# 가계부 상세내용
class AccountDetail(TimeStampModel):
    account_category = models.ForeignKey('AccountCategory', related_name='account_details', verbose_name='카테고리', null=True, on_delete=models.DO_NOTHING)
    account_book = models.ForeignKey('AccountBook', verbose_name='가계부', on_delete=models.CASCADE)
    written_date = models.DateTimeField()
    price = models.DecimalField(max_digits=9, decimal_places=0)
    description = models.CharField(blank=True, null=True, max_length=255)
    account_type = models.CharField(max_length=10) # 수입, 지출 구분
    delete_flag = models.BooleanField(default=False)

    class Meta:
        db_table = 'account_detail'

    def __str__(self):
        return f'book_name: {self.account_book.book_name} / price: {self.price}'

# 가계부 카테고리
class AccountCategory(TimeStampModel, DeleteFlag):

    category_name = models.CharField(max_length=50) 
    user = models.ForeignKey('users.User', related_name='categories', verbose_name='유저', on_delete=models.CASCADE)
    delete_flag = models.BooleanField(default=False)
    class Meta:
        db_table = 'account_category'

    def __str__(self):
        return self.category_name