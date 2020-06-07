from django.contrib import admin

# Register your models here.
from .models import Tshirt, User

admin.site.register(Tshirt)
admin.site.register(User)
