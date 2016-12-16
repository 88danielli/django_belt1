from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add_user$', views.add_user),
    url(r'^quotes$', views.quotes),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quote_process$', views.quote_process),
    url(r'^users/(?P<id>\d+)$', views.users),
    url(r'^favorite_process$', views.favorite_process)
]
