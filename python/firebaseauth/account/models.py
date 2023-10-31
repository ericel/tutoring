from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    uid = models.CharField(max_length=191, null=False, unique=True)
    username = models.CharField(max_length=150, null=False, unique=True)
    first_name = models.CharField(max_length=120, default="", blank=True)
    last_name = models.CharField(max_length=120, default="", blank=True)
    about_me = models.TextField(max_length=225, default="About me text", blank=True)
    is_active = models.BooleanField(default=True)  # can login
    is_verified = models.BooleanField(default=False)  # can login
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    class Meta:
        pass
    
    def __str__(self):
        return f"{self.username} user account last updated at:- {self.updated_at}"

    def __init__(self, *args, **kwargs):
        super(CustomUser, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
    
    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)
