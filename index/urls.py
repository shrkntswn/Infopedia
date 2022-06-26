from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name="search" ),
    path('auto_search/', views.auto_search, name='auto_search'),
    path('home/', views.home, name="home"),
    path('category/<int:id>/<str:category>/', views.category, name="category"),
    path('create/', views.main_article_create, name="main_article_create"),
    path('create/<int:id>', views.sub_article_create, name="sub_article_create"),
    path('update/<int:id>/', views.article_update, name="article_update"),
    path('sub-article-update/<int:id>/', views.sub_article_update, name="sub_article_update"),
    path('<int:id>/<slug:slug>/', views.article_detail, name="article_detail"),
    path('add_category', views.add_category, name="add_category"),
    path('rollback/<int:id>', views.rollback, name="rollback"),
    path('random_article',views.random_article, name="random_article"),
    path('delete/<int:id>', views.article_delete, name="article_delete"),
    path('sub_article_delete/<int:id>/<int:art_id>/<slug:slug>', views.sub_article_delete, name="sub_article_delete")
]