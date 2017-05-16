# website/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
# from django.views.generic.detail import DetailView
from django.views import generic
from .models import Project, Upload

# Create your views here.
# class HomePageView(TemplateView):
#     def get(self, request, **kwargs):
#         return render(request, 'index.html', context=None)


class HomePageView(TemplateView):

    def get(self, request, **kwargs):
        projects = Project.objects.all()
        # for project in projects:
        #     print(project.title)
        return render(request, 'index.html', {
            'projects': projects,
        })


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'project_detail.html'
