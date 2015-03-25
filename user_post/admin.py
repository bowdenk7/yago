from user_post.models import Post, ReportedPost, Like
from django.contrib import admin

admin.site.register(Post)

admin.site.register(ReportedPost)

admin.site.register(Like)