from django.db import models
from django.template.defaultfilters import slugify


# organize between properties and methods
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

    def get_cover_photo(self):
        photo = Photo.objects.filter(project=self).get(is_cover_photo=True)
        return photo.image


def get_image_path(instance, filename):
    return '/'.join(['project_images', instance.project.slug, filename])


class Photo(models.Model):
    project = models.ForeignKey(Project, related_name="photos")
    image = models.ImageField(upload_to=get_image_path)
    is_cover_photo = models.BooleanField()
    caption = models.TextField(blank=True)

    # def __str__(self):
    #     return self.image.name



    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Project, self).save(*args, **kwargs)

    # # Use reverse() to give you the url of a page, given the path to the view.
    # def get_absolute_url(self):
    #     return reverse('website.views.project_details', args=[str(self.id)])


