from django.contrib import admin
from .models import User, Friend

my_models = [User, Friend]

admin.site.register(my_models)
