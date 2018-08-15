from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^success$', views.success, name='success'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$',views.logout,name='logout'),
    url(r'^wall$',views.wall,name='wall'),
    url(r'^new_message$',views.new_message,name='new_message'),
    url(r'^new_comment$',views.new_comment,name='new_comment'),
]
