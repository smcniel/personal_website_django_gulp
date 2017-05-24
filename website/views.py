# website/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views import generic
from .models import Project, Photo
# from django.db.models import Prefetch
from braces.views import PrefetchRelatedMixin

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# @cache_page(CACHE_TTL)
@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class HomePageView(TemplateView):

    def get(self, request, **kwargs):

        projects = Project.objects.all(
        ).prefetch_related(
            'photos__project',
        ).all()

        # ).all().filter(photos__is_cover_photo=True)
        # Prefetch(
    #             'photos_set',
    #             queryset=Photo.objects.filter(is_cover_photo=False),
    #             to_attr="proj_imgs"
    #         ),
        return render(request, 'index.html', {
            'projects': projects,
        })


class ProjectDetailView(PrefetchRelatedMixin, generic.DetailView):
    model = Project
    template_name = 'project_detail.html'
    prefetch_related = ['photos']

    # photo = Photo.objects.selected_related('project').all()
    # for photo in photos:
    #     return photo

    # def get_queryset(self):
    #     self.queryset = super(ProjectDetailView, self).get_queryset()
    #     print(self.queryset)
    #     return self.queryset
    # def get_queryset(self):
    #     self.project = get_object_or_404(Project, name=self.args[0])
    #     return Photo.objects.filter(project=self.project)

    # def get_object(self):
    #     obj = self.queryset.get()
    #     print(obj)
    #     return obj

    # photos.images_set.filter(is_cover_photo=False)

    # def get_queryset(self):
    #     qs = super(ProjectDetailView, self).get_queryset().prefetch_related('photos_set')
    #     qs.filter(photo)

    # def get_queryset(self):
    #     # returns project images that are not cover images
    #     return super(ProjectDetailView, self).get_queryset().prefetch_related(
    #         Prefetch(
    #             'photos_set',
    #             queryset=Photo.objects.filter(is_cover_photo=False),
    #             to_attr="proj_imgs"
    #         ),
    #     )
