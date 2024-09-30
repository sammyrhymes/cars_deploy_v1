from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='user-profile'),
    path('profile/update/', views.profile_update, name='user-profile-update'),
]