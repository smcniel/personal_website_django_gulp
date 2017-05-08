# website/urls.py
from django.conf.urls import url
from website import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    # url(r'^projects/(?P<slug>[-\w]+)/$', views.ProjectDetailView.as_view(),
    #     name='project_detail'),
    url(r'^(?P<slug>[-\w]+)/$', views.ProjectDetailView.as_view(),
        name='project_detail'),
    # url(r'^projects/(?P<slug>[-\w]+)/$', views.ProjectPageView.as_view()),
    # url(r'^project_page/$', views.ProjectPageView.as_view(), name='project_page'),
]
