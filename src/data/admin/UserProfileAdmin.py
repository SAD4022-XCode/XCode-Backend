from django.contrib import admin
from ..models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'birth_date']
    list_select_related = ['user']

    def user_info(self, profile: UserProfile):
        return f'{profile.user.first_name} {profile.user.last_name}'