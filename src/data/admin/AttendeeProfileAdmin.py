from django.contrib import admin
from ..models import AttendeeProfile

@admin.register(AttendeeProfile)
class AttendeeProfileAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'birth_date']
    list_select_related = ['user']

    def user_info(self, attendee: AttendeeProfile):
        return attendee.user.full_name