from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('artists/', views.Artists.as_view(), name='artists'),
    path('artists/<str:artist>/', views.Artists.as_view()),
    path('events/', views.Events.as_view(), name='events'),
    path('events/<str:event_id>/', views.EventById.as_view(), name='events'),
    path('notifications/', views.Notifications.as_view(), name='notifications'),
    path('notifications/<str:action>/', views.Notifications.as_view(), name='notifications'),
    path('spotify/', views.Spotify.as_view(), name='spotify'),
    path('user_preferences/', views.UserPreferences.as_view(), name='user_preferences'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login')
]
