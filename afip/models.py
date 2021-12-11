from django.db import models

# Create your models here.
class Status(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    app = models.BooleanField()
    db = models.BooleanField()
    auth = models.BooleanField()

    def is_up(self):
        return self.app and self.db and self.auth
