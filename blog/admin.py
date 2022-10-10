from django.contrib import admin
from .models import Post

# Register your models here.

@admin.registewr(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "slug"]
    prepopulated_fields = {'slug': ('title',)}
