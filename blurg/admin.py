from django.contrib import admin
from blurg.models import Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    
admin.site.register(Category, CategoryAdmin)