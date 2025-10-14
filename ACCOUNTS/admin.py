from django.contrib import admin

from .models import user

class CustomUserAdmin(admin.ModelAdmin):
    model=user
    list_display=('username','email')
admin.site.register(user, CustomUserAdmin)