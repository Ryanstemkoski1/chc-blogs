from django.contrib import admin
from tag.models import FailedPost, Post

class PostAdmin(admin.ModelAdmin):
    list_display = ["post_id", "post_title", "post_content"]
    fieldsets = [
        # (None, {"fields": ["product_url"]}),
        ("Post Id", {"fields": ["post_id"]}),
        ("Post Title", {"fields": ["post_title"]}),
        ("Post Content", {"fields": ["post_content"]}),
        ("Tags", {"fields": ["tags"]}),
        ("Categories", {"fields": ["categories"]}),
    ]
    search_fields = ['post_id', 'post_title', 'post_content']


admin.site.register(Post, PostAdmin)

class FailedPostAdmin(admin.ModelAdmin):
    list_display = ["post_id", "post_title", "post_content"]
    fieldsets = [
        # (None, {"fields": ["product_url"]}),
        ("Post Id", {"fields": ["post_id"]}),
        ("Post Title", {"fields": ["post_title"]}),
        ("Post Content", {"fields": ["post_content"]}),
    ]
    search_fields = ['post_id', 'post_title', 'post_content']


admin.site.register(FailedPost, FailedPostAdmin)
