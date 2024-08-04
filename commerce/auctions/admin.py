from django.contrib import admin

from .models import Listing, Category, User, Comments
# Register your models here.

admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Comments)
