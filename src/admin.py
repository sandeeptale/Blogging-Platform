from django.contrib import admin
from .models import *


admin.site.register(blog)
admin.site.register(blog_category)
admin.site.register(subcription)



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'phone', 'email')
    list_per_page = 20

admin.site.register(user_profile, UserProfileAdmin)

