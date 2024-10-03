from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='user-profile'),
    path('profile/update/', views.profile_update, name='user-profile-update'),
    path('deposit/', views.deposit, name='deposit'),
    path('deposit_stk/', views.deposit_stk, name='deposit_stk'),    
]