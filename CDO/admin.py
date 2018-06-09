from django.contrib import admin

from CDO.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]
    list_filter = ['user_permission']

    class Meta:
        model = User


class OrgAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Organisation._meta.fields]
    list_filter = ['org_id']

    class Meta:
        model = Organisation


admin.site.register(User, UserAdmin)
admin.site.register(Organisation, OrgAdmin)
