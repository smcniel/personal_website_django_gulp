from django.contrib import admin
from website.models import Project, Photo


# Set up automated slug creation
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('title', 'description', 'order',)
    prepopulated_fields = {'slug': ('title',)}


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('project', 'is_cover_photo', 'caption')
    list_display_links = ('project',)

# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Photo, PhotoAdmin)
