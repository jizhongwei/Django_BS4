from django.urls import path, include

from . import views

app_name = 'article'
urlpatterns = [
    path('article-list', views.article_list, name = 'article-list'),
]