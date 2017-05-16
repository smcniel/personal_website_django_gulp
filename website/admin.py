from django.contrib import admin
from website.models import Project, Upload


# Set up automated slug creation
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('title', 'description',)
    prepopulated_fields = {'slug': ('title',)}


class UploadAdmin(admin.ModelAdmin):
    list_display = ('project', )
    list_display_links = ('project',)
# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Upload, UploadAdmin)
