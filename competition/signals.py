from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from .models import BasketItem, Competition

@receiver(user_logged_in)
def merge_basket_after_login(request, user, **kwargs):
    session_basket = request.session.pop('basket_before_login', [])

    if session_basket:
        # Merge the session basket with the authenticated user's basket
        for item in session_basket:
            competition = Competition.objects.get(id=item['competition_id'])
            basket_item, created = BasketItem.objects.get_or_create(
                user=user,
                competition=competition,
                defaults={'ticket_count': item['ticket_count']}
            )
            if not created:
                # If item already exists, update the ticket count
                basket_item.ticket_count += item['ticket_count']
                basket_item.save()

        # Optionally, clear the session basket after merging
        request.session['basket'] = []