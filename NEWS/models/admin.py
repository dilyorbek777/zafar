from django.contrib import admin
from .models import *

admin.site.register([Category, Contact, Food, Cheifs])


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'publish_time']
    list_filter = ['publish_time']
    prepopulated_fields = {'slug': ['title']}
    date_hierarchy = 'publish_time'
    search_fields = ['title', 'body']
    ordering = ['publish_time', 'status']


