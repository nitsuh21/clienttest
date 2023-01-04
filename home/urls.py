from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('',views.cloudservers,name='cloudservers'),
    path('fun',views.fun,name='fun'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('console/<str:name>/',views.console,name='console'),
    path('summary/<str:name>/',views.summary,name='summary'),
    path('backup/<str:name>/',views.backup,name='backup'),
    path('snapshots/<str:name>/',views.snapshots,name='snapshots'),
    path('cloudservers',views.cloudservers,name='cloudservers'),
]
