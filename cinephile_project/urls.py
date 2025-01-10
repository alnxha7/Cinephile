"""
URL configuration for cinephile_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cinephile import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register_user/', views.register_user, name='register_user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('critics_index/', views.critics_index, name='critics_index'),
    path('agency_index/', views.agency_index, name='agency_index'),
    path('admin_index/', views.admin_index, name='admin_index'),
    path('aspirant_index/', views.aspirant_index, name='aspirant_index'),

    path('user_approval/', views.user_approval, name='user_approval'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('edit_movie/<int:movie_id>', views.edit_movie, name='edit_movie'),

    path('critics_view_movies/', views.critics_view_movies, name='critics_view_movies'),
    path('review_movie/<int:movie_id>', views.review_movie, name='review_movie'),
    path('admin_manage_reviews/<int:movie_id>', views.admin_manage_reviews, name='admin_manage_reviews'),
    path('delete_review/<int:movie_review_id>', views.delete_review, name='delete_review'),

    path('aspirant_view_movies/', views.aspirant_view_movies, name='aspirant_view_movies'),
    path('aspirant_review/<int:movie_id>', views.aspirant_review, name='aspirant_review'),
    path('aspirant_posts/', views.aspirant_posts, name='aspirant_posts'),
    path('post_details/<int:post_id>', views.post_details, name='post_details'),

    path('post_approval/', views.post_approval, name='post_approval'),
    path('all_posts/', views.all_posts, name='all_posts'),
    path('agency_react/<int:post_id>', views.agency_react, name='agency_react'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)