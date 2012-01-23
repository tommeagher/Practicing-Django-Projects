from django.contrib import admin
from blurg.models import Category, Entry

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    
class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}

admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)
