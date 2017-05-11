from django.db import models
# from django.utils import timezone
from django.template.defaultfilters import slugify

# organize between properties and methods
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(unique=True)

# def get_image_path(instance, filename):
#     return '/'.join(['project_images', instance.project.slug, filename])

# class Upload(models.Model):
#     project = models.ForeignKey(Project, related_name="uploads")
#     image = models.ImageField(upload_to=get_image_path)




    # def __str__(self):
    #     return self.title

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Project, self).save(*args, **kwargs)

    # # Use reverse() to give you the url of a page, given the path to the view.
    # def get_absolute_url(self):
    #     return reverse('website.views.project_details', args=[str(self.id)])


