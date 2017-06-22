from django.db import models
# from embed_video.fields import EmbedVideoField


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


def get_image_path(instance, filename):
    return '/'.join(['project_images', instance.project.slug, filename])


class Photo(models.Model):
    project = models.ForeignKey(Project, related_name="photos")
    image = models.ImageField(upload_to=get_image_path)
    is_cover_photo = models.BooleanField()
    caption = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)


# class Photo(models.Model):
#     project = models.ForeignKey(Project, related_name="photos")
#     image = models.ImageField(upload_to=get_image_path)
#     is_cover_photo = models.BooleanField()
#     caption = models.TextField(blank=True)


# class Video(models.Model):
#     project = models.ForeignKey(Project, related_name="videos")
#     video = EmbedVideoField()  # similar to models.URLField()


