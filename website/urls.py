# website/urls.py
from django.conf.urls import url
from website import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    # url(r'^projects/(?P<slug>[-\w]+)/$', views.ProjectDetailView.as_view(),
    #     name='project_detail'),
    url(r'^(?P<slug>[-\w]+)/$', views.ProjectDetailView.as_view(),
        name='project_detail'),
    # url(r'^projects/(?P<slug>[-\w]+)/$', views.ProjectPageView.as_view()),
    # url(r'^project_page/$', views.ProjectPageView.as_view(), name='project_page'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += [
#         url(r'^media/(?P<path>.*)$', 'django.views.static.serve', \
#             {
#                 'document_root': settings.MEDIA_ROOT,
#             }),
#     ]

# if settings.DEBUG:
#     urlpatterns += patterns(
#         'django.views.static',
#         (r'^media/(?P<path>.*)',
#         'serve',
#         {'document_root': settings.MEDIA_ROOT}), )
