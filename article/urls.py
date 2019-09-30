from django.urls import path, include

from . import views

app_name = 'article'
urlpatterns = [
    path('article-list', views.article_list, name = 'article-list'),
    path('article-detail/<int:id>/', views.article_detail, name = 'article-detail'),
    path('article-create/', views.article_create, name = 'article-create'),
    path('article-delete/<int:id>/', views.article_delete, name = 'article-delete'),
]