from django.contrib import admin

from .models import *

admin.site.register(CustomUser)
admin.site.register(Bookmarks)
admin.site.register(News)
admin.site.register(Comments)
