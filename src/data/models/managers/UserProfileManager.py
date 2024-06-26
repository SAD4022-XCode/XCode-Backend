from django.db import models

class UserProfileManager(models.Manager):

    def get_by_id(self, id):
        return self.select_related("user").get(user_id = id)