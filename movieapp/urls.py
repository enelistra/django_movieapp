from django.shortcuts import render
from django import views
from django.contrib import admin
from django.urls import include,path
from .import views

urlpatterns = [
    path('',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('index/',views.index,name='index'),
    path('details/<int:movie_id>/',views.details,name='details'),
    path('search/',views.search, name='search'),
    path('logout/',views.user_logout,name='logout'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('adminindex/',views.adminindex,name='adminindex'),
    path('adminadd/',views.adminadd, name='adminadd'),
    path('adminview/',views.adminview,name='adminview'),
    path('admindetails/<int:movie_id>/',views.admindetails,name='admindetails'),
    path('update_movies/<int:movie_id>/',views.update_movies,name='update_movies'),
    path('delete/<int:movie_id>/',views.delete,name='delete'),
    path('review/<int:movie_id>/',views.review,name='review'),
    path('replys/<int:movie_id>/', views.replys, name='replys'),
    path('viewuser/', views.viewuser, name='viewuser'),
    path('deleteuser/<int:user_id>/',views.deleteuser,name='deleteuser'),
    path('mywatchlist/', views.mywatchlist, name='mywatchlist'),
    path('remove_from_watchlist/<int:movie_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('newwatchlist/', views.mywatchlist, name='newwatchlist'),
    path('viewprofile/',views.viewprofile,name='viewprofile'),
]