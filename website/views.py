# website/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
# from django.views.generic.detail import DetailView
from django.views import generic
from .models import Project

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

# class ProjectDetail(TemplateView):
#     # projects = Project.objects.all()

#     def get(self, request, slug):
#         project = Project.objects.get(slug=slug)
#         return render(request, 'projects/project_detail.html', {
#             'project': project,
#         })

    # def dispatch(self, request, *args, **kwargs):
    #     print(projects.title)


    # def get_context_data(self, **kwargs):
    #     context = super(ProjectPageView, self).get_context_data(**kwargs)
    #     if now().weekday() < 5 and 8 < now().hour < 18:
    #         context['open'] = True
    #     else:
    #         context['open'] = False
    #     return context

# class ProjectDetails()
