from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('artists/', views.Artists.as_view(), name='artists'),
    path('artists/<str:artist>/', views.Artists.as_view()),
    path('events/', views.Events.as_view(), name='events'),
    path('notifications/', views.Notifications.as_view(), name='notifications'),
    path('spotify/', views.Spotify.as_view(), name='spotify'),
]
