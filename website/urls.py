# website/urls.py
from django.conf.urls import url
from website import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
]
