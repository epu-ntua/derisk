from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^overview', views.overview, name='overview'),
    url(r'^projects/$', views.ProjectListView.as_view(), name='project-list'),
    url('^projects/(?P<pk>[\w-]+)$', views.ProjectUpdate.as_view(), name='project-edit'),
    url('^projects/delete/(?P<pk>[\w-]+)$', views.ProjectDelete, name='project-delete'),
    url('^projects/create/$', views.ProjectCreate, name='project-create'),
]