from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),    
    # path('user_auth/', views.user_auth, name='user_auth'),
    path('create-stripe-session/', views.create_stripe_checkout_session, name='create_stripe_session'),
    path('test/', views.test, name='test'),
    # path('profile/', views.profile_view, name='profile'),
    path('view_wallet/', views.wallet, name='view_wallet'),
    path('competitions/', views.competitions, name='competitions'),
    path('competition/<int:competition_id>/', views.competition_details, name='competition'),
    path('competition/<int:id>/add_to_basket/', views.add_to_basket, name='add_to_basket'),
    path('basket/', views.view_basket, name='view_basket'),
    path('check_out/', views.check_out, name = 'check_out'),
    path('stk/', views.stk, name="stk"),
    path('DPO/', views.DPO_payment, name="DPO"),
    path('stripe/', views.stripe_payment, name="stripe"),
    path('base/', views.base, name='base'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failed/', views.payment_failure, name='payment_failure'),
    path('remove_from_basket/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),
      ]