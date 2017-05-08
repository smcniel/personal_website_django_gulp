from django.contrib import admin
from website.models import Project


# Set up automated slug creation
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('title', 'description',)
    prepopulated_fields = {'slug': ('title',)}

# Register your models here.
admin.site.register(Project, ProjectAdmin)
