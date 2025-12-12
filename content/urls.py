"""
URL configuration for the content application.

Routes:
    - / : Homepage with latest devlogs and featured projects
    - /explore/ : Grid view of featured projects with associated devlogs and search
    - /devlog/<slug>/ : Individual devlog detail page
    - /project/<slug>/ : Individual project detail page
    - /rss/ : RSS feed of published devlogs
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore_grid, name='explore_grid'),
    path('devlog/<slug:slug>/', views.devlog_detail, name='devlog_detail'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('rss/', views.rss_feed, name='rss_feed'),
]
