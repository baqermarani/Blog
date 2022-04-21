from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.IndexPage.as_view() , name='index'),
    path('contact/', views.ContactPage.as_view() , name='contact'),
    path('article/' , views.SingleArticle.as_view() , name='single_article'),
    path('article/all/', views.AllArticleAPIViwe.as_view() , name='all_articles'),
    path('article/search/', views.SearchArticleAPIViwe.as_view() , name='search_articles'),
    path('article/submit/', views.SubmitArticleAPIView.as_view(), name='submit_article'),
    path('article/update-cover/', views.UpdateArticleAPIView.as_view(), name='update_article'),
    path('article/delete/', views.DeleteArticleAPIView.as_view(), name='delete_article'),
]