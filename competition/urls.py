from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),    
    # path('create-stripe-session/', views.create_stripe_checkout_session, name='create_stripe_session'),
    path('test/', views.test, name='test'),
    path('editCompetition/<int:pk>/', views.editCompetition, name='editCompetition'),
    path('editholidayCompetition/<int:pk>/', views.editholidayCompetition, name='editholidayCompetition'),
    path('deleteCompetition/<int:pk>/', views.deleteCompetition, name='deleteCompetition'),
    path('deleteholidayCompetition/<int:pk>/', views.deleteholidayCompetition, name='deleteholidayCompetition'),
    path('deleteImage/<int:pk>/', views.deleteImage, name='deleteImage'),
    path('deleteholidayImage/<int:pk>/', views.deleteholidayImage, name='deleteholidayImage'),
    path('listUsers/', views.listUser, name='listUsers'),
    path('listCompetitions/', views.listCompetitions, name='listCompetitions'),
    path('listHolidayCompetitions/', views.listHolidayCompetitions, name='listHolidayCompetitions'),
    path('createCompetition/', views.create_competition, name='createCompetition'),
    path('createholiCompetition/', views.create_holiday_competition, name='createholiCompetition'),
    path('view_wallet/', views.wallet, name='view_wallet'),
    path('competitions/', views.competitions, name='competitions'),
    path('holicompetitions/', views.holidaycompetitions, name='holicompetitions'),
    path('holicompetition/<int:holicompetition_id>/', views.holicompetition_details, name='holicompetition'),
    path('competition/<int:competition_id>/', views.competition_details, name='competition'),
    path('competition/<int:id>/add_to_basket/', views.add_to_basket, name='add_to_basket'),
    path('holicompetition/<int:id>/add_to_baskety/', views.add_to_baskety, name='add_to_baskety'),
    path('update-basket/', views.update_basket, name='update_basket'),
    path('basket/', views.view_basket, name='view_basket'),
    path('check_out/', views.check_out, name = 'check_out'),
    path('stk/', views.stk, name="stk"),
    path('DPO/', views.DPO_payment, name="DPO"),
    # path('paypal/', views.paypal, name='paypal'),
    # path('stripe/', views.stripe_payment, name="stripe"),
    path('base/', views.base, name='base'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failed/', views.payment_failure, name='payment_failure'),
    path('remove_from_basket/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),
    path('create_payment/', views.create_payment, name='create_payment'),
    path('execute_payment/', views. execute_payment, name='execute_payment'),
      ]