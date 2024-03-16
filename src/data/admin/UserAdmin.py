from django.contrib import admin
from ..models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_fieldsets = (
        (None, {
            'classes' : ('wide', ),
            'fields' : ('username', 'password1', 'password2', 'email', 'full_name')
            }
        ),
    )