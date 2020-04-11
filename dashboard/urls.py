from django.conf.urls import url
from dashboard import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^disconnect/', views.disconnect, name='disconnect'),
    url(r'^config/', views.app_config_page, name='config'),
    url(r'^edit_login/', views.edit_login_page, name='edit_login'),
    url(r'^edit_fb_access/', views.edit_facebook_app, name='edit_fb_access'),
    url(r'^campagne/(?P<cmp_id>[0-9]+)$', views.campagne_detail_page, name='detail'),
    url(r'^edit_fb_page/(?P<page_id>[0-9]+)$', views.edit_facebook_page, name='page_detail'),
    url(r'^campagne/', views.campagne_home_page, name='campagne'),
    url(r'^ajax/fb_query', views.campagne_control_dashboard, name='fb_query'),
]