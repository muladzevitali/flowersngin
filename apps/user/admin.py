from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email', 'created')
    readonly_fields = ('created', )
    ordering = ('-created',)


admin.site.register(User, UserAdmin)
admin.site.register(Contact, ContactAdmin)
