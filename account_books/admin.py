from django.contrib import admin

from .models import AccountBook, AccountCategory, AccountDetail

# Register your models here.
admin.site.register(AccountBook)
admin.site.register(AccountDetail)
admin.site.register(AccountCategory)
