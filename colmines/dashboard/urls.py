from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url(r'^$', views.custom_login),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='logout'),

    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^reportes', views.reportes, name='reportes'),
    url(r'^alertas', views.alertas, name='alertas'),
    url(r'^actuadores', views.actuador, name='actuadores'),
    url(r'^actuales/(?P<nivel>[0-9]+)/(?P<area>[0-9]*)', views.actuales, name='actuales'),
    url(r'^micros/(?P<id>[0-9]+)/(?P<tipo>[a-z]+)$', views.grafica),
    url(r'^make_plot/(?P<id>[0-9]+)/(?P<tipo>[a-z]+)$', views.make_plot),

    url(r'^rest/ubicaciones$', views.ubicacion_list),
    url(r'^rest/ubicaciones/(?P<pk>[0-9]+)$', views.ubicacion_detail),

    url(r'^rest/tipos/$', views.tipo_list),
    url(r'^rest/tipos/(?P<pk>[0-9]+)$', views.tipo_detail),

    url(r'^rest/micro$', views.micro_list),
    url(r'^rest/micro/(?P<pk>[0-9]+)$', views.micro_detail),

    url(r'^rest/alertas/sensores$', views.alerta_list),
    url(r'^rest/alertas/sensores/(?P<pk>[0-9]+)$', views.alerta_detail),

    url(r'^rest/alertas/actuador$', views.alertaAct_list),
    url(r'^rest/alertas/actuador/(?P<pk>[0-9]+)$', views.alertaAct_detail),


    url(r'^rest/mediciones$', views.medicion_list),
    url(r'^rest/mediciones/(?P<pk>[0-9]+)$', views.medicion_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)
