from django.contrib import admin
from authentication.models import CustomUser

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    pass
