from django.contrib import admin
from .models import Stock, Account, OwnStock
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_admin', 'date_joined')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



admin.site.register(Stock)
admin.site.register(Account, AccountAdmin)
admin.site.register(OwnStock)
