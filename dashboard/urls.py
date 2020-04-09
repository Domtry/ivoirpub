from django.conf.urls import url
from dashboard import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^disconnect/', views.disconnect, name='disconnect'),
    url(r'^campagne/(?P<cmp_id>[0-9]+)$', views.campagne_detail_page, name='detail'),
    url(r'^campagne/', views.campagne_home_page, name='campagne'),
]