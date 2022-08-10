from __future__ import unicode_literals

from django.contrib import admin
from shopping.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.register(User)