from django.conf.urls import url
from django.urls import path

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('peticios/', views.PeticioListView.as_view(), name='peticions'),
    path('peticio/<uuid:pk>', views.PeticioDetailView.as_view(), name='peticio-detail'),
    path('concesio/<int:pk>', views.ConcesioDetailView.as_view(), name='concesio-detail'),
    path('concesios/', views.ConcesioListView.as_view(), name='concesions'),
    #url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
]

urlpatterns += [
    path('peticio/new', views.peticio_new, name='peticio_new'),
    path('peticio/<uuid:pk>/servir/', views.peticio_servir, name='peticio_servir'),]
