from django.conf.urls import url
from dashboard import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^disconnect/', views.disconnect, name='disconnect'),
    url(r'^config/', views.app_config_page, name='config'),
    url(r'^edit_login/', views.edit_login_page, name='edit_login'),
    url(r'^campagne/(?P<cmp_id>[0-9]+)$', views.campagne_detail_page, name='detail'),
    url(r'^campagne/', views.campagne_home_page, name='campagne'),
    url(r'^ajax/fb_query', views.campagne_control_dashboard, name='fb_query'),
    url(r'^ajax/data', views.facebook_control_dashboard, name='fb_data'),
]