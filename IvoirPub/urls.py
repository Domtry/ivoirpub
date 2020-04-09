from django.conf.urls import url, include
from dashboard import views, urls

urlpatterns = [
    url(r'^$', views.login_page, name='login'),
    url(r'^login/', views.login_page, name='login'),
    url(r'^register/', views.registre_page, name='register'),
    url(r'^init_config/', views.init_config, name='init_config'),
    url(r'^forget/', views.forget_password_page, name='forget-pass'),
    url(r'^dashboard/', include(('dashboard.urls', 'dashboard_app'), namespace='dashboard_sp')),   
]
