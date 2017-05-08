from django.db import models
# from django.utils import timezone
from django.template.defaultfilters import slugify

# organize between properties and methods
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    # def __str__(self):
    #     return self.title

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Project, self).save(*args, **kwargs)

    # # Use reverse() to give you the url of a page, given the path to the view.
    # def get_absolute_url(self):
    #     return reverse('website.views.project_details', args=[str(self.id)])


