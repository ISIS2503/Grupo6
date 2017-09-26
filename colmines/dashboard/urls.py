from django.conf.urls import url

from . import views

#urlpatterns = [
#    url(r'^ubicaciones/$', views.ubicacion_list),
#    url(r'^ubicaciones/(?P<pk>[0-9]+)/$', views.ubicacion_list),
#]
#urlpatterns = [
#    url(r'^tipos/$', views.tipo_list),
#    url(r'^tipos/(?P<pk>[0-9]+)/$', views.tipo_list),
#]

urlpatterns = [
    url(r'^sensores/$', views.sensor_list),
    url(r'^sensores/(?P<pk>[0-9]+)/$', views.sensor_list),
]
