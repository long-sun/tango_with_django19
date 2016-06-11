from django.contrib import admin
from rango.models import Category, Page

class PageInline(admin.TabularInline):
    model = Page
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('views and likes', {'fields': ['views', 'likes']})
        ]
    inlines = [PageInline]
    list_display = ('name', 'views', 'likes')

class PageAdmin(admin.ModelAdmin):
    #fields = ['category', 'title', 'url', 'views']
    fieldsets = [
        (None, {'fields': ['category']}),
        ('Detail information', {'fields': ['title', 'url', 'views']})
        ]
    list_display = ('category', 'title', 'url')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)