from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ubicaciones/$', views.ubicacion_list),
    url(r'^ubicaciones/(?P<pk>[0-9]+)/$', views.ubicacion_list),

    url(r'^tipos/$', views.tipo_list),
    url(r'^tipos/(?P<pk>[0-9]+)/$', views.tipo_list),

    url(r'^sensores/$', views.sensor_list),
    url(r'^sensores/(?P<pk>[0-9]+)/$', views.sensor_list),
    
    url(r'^sensoresUb/$', views.sensor_ubicacion_list),
    url(r'^sensoresUb/(?P<pk>[0-9]+)/$', views.sensor_ubicacion_list),
]
