from django.contrib import admin
from .models import post,Comment
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','post','created','active')
    search_fields = ('name','email','body')
    list_filter = ('active','created','updated')
    ordering = ['active','created']
admin.site.register(Comment,CommentAdmin)

class postAdmin(admin.ModelAdmin):
    list_display = ('title','author','publish','status')
    search_fields = ('title',)
    prepopulated_fields = { 'slug' : ('title',)}
    ordering = ['status','publish']
    list_filter = ('status','publish','created','author',)
admin.site.register(post, postAdmin)