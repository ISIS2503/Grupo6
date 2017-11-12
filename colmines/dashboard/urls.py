from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='logout'),

    url(r'^dashboard', views.dashboard),

    url(r'^ubicaciones$', views.ubicacion_list),
    url(r'^ubicaciones/(?P<pk>[0-9]+)$', views.ubicacion_detail),

    url(r'^tipos/$', views.tipo_list),
    url(r'^tipos/(?P<pk>[0-9]+)$', views.tipo_detail),

    url(r'^micro$', views.micro_list),
    url(r'^micro/(?P<pk>[0-9]+)$', views.micro_detail),

    url(r'^alertas/sensores$', views.alerta_list),
    url(r'^alertas/sensores/(?P<pk>[0-9]+)$', views.alerta_detail),

    url(r'^alertas/actuador$', views.alertaAct_list),
    url(r'^alertas/actuador/(?P<pk>[0-9]+)$', views.alertaAct_detail),


    url(r'^mediciones$', views.medicion_list),
    url(r'^mediciones/(?P<pk>[0-9]+)$', views.medicion_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)
