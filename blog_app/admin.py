from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_date', 'updated_date',)
    # filter_horizontal = ('categories', 'tags')

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     return request.user.is_superuser


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_date', 'updated_date')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_date', 'updated_date')
