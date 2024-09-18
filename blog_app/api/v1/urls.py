from django.urls import path
from . import views

app_name = 'blog_app_api_v1'


urlpatterns = [
    path('articles/', views.ArticleListApiView.as_view(), name='articles'),
    path('articles/<int:pk>/', views.ArticleDetailApiView.as_view(), name='article_detail'),
    path('articles/create/', views.ArticleCreateApiView.as_view(), name='article_create'),
    path('categories/', views.CategoryListApiView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoryDetailApiView.as_view(), name='category_detail'),
]
