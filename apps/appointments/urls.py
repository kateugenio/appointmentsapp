from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^appointments$', views.showDashboard),
    url(r'^addappt$', views.create),
    url(r'^appointments/(?P<id>\d+)$', views.editAppt),
    url(r'^appointments/update/(?P<id>\d+)$', views.updateAppt),
    url(r'^appointments/delete/(?P<id>\d+)$', views.deleteAppt),
	url(r'^logout$', views.logout),
]