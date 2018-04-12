from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('artists/', views.Artists.as_view(), name='artists'),
    path('artists/<str:artist>/', views.Artists.as_view()),
    path('events/', views.events, name='events'),
]
