from django.contrib import admin
from django.urls import path, include
from node_display import views

app_name = 'node_display'

urlpatterns = [
    path('', views.index, name='index'),
    path('accepted/', views.get_accepted_node, name='get_accepted_node'),
    path('pending/', views.get_pending_node, name='get_pending_node'),
    path('all/', views.get_all_node, name='get_all_node'),
    path('server/', views.server_info_submit, name='server_info_submit'),
    path('properties/<str:hostname>/<slug:id>/', views.properties, name='properties'),
]
