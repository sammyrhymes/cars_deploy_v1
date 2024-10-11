from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import datetime

from django.contrib.auth.decorators import login_required
from .models import *

from xml.etree import ElementTree as ET

DPO_COMPANY_TOKEN = '84B57785-1C87-48F1-9B0B-2781862D8671'  # Replace with actual token
DPO_BASE_URL = 'https://secure.3gdirectpay.com/API/v6/'



# Authentication models and functions
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login


import json
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse

from competition.credentials import LipanaMpesaPpassword, MpesaAccessToken, MpesaC2bCredential

import requests
import time
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages

# import stripe
# from django.conf import settings
# from django.shortcuts import render
# from .models import BasketItem

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#paypal settings
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from user.models import *
from django.db.models import Count

# Create your views here.

def admin_dashboard(request):

    user_list = User.objects.all()[:3]
    user_count = User.objects.all().count()
    competition_list = Competition.objects.all()[:3]
    competition_count = Competition.objects.count()
    holidays = HolidayCompetition.objects.all()
    regular_users_count = User.objects.filter(is_staff=False, is_superuser=False).count()
    admin_users_count = User.objects.filter(is_staff=True, is_superuser=True).count()
    # mpesa = MpesaTransaction.objects.all()
    competitions = CompetitionImage.objects.all()
    # competitions = Entry.objects.all()
    # competitions = Ticket.objects.all()
    # competitions = Winner.objects.all()
    # competitions = ContactInquiry.objects.all()
    # competitions = BlogPost.objects.all()
    # competitions = FAQ.objects.all()
    # competitions = BasketItem.objects.all()
    context = {
        'competition_count':competition_count,
        'competition_list':competition_list,
        'user_list':user_list,
        'user_count': user_count,
        'regular_users_count':regular_users_count,
        'admin_users_count': admin_users_count,

    }


    return render(request, 'frontend/admin.html',context)


def create_competition(request):
    if request.method == 'POST':
        competition_form = CompetitionForm(request.POST, request.FILES)
        image_form = CompetitionImageForm(request.POST, request.FILES)

        if competition_form.is_valid() and image_form.is_valid():
            competition = competition_form.save()


            # Handle multiple images
            for image in image_form.cleaned_data['images']:
                CompetitionImage.objects.create(competition=competition, image=image)

            messages.success(request, "Competition created successfully!")
            return redirect('createCompetition')  # Redirect to the same page or a success page
    else:
        competition_form = CompetitionForm()
        image_form = CompetitionImageForm()

    context = {
        'competition_form': competition_form,
        'image_form': image_form,
    }
    
    return render(request, 'frontend/createCompetition.html', context)


def listCompetitions(request):
    competition_list = Competition.objects.annotate(player_count=Count('entries'))    
    competition_count = competition_list.count()
    user_list = User.objects.all()
    user_count = User.objects.all().count()
    holidays = HolidayCompetition.objects.all()
    regular_users_count = User.objects.filter(is_staff=False, is_superuser=False).count()
    admin_users_count = User.objects.filter(is_staff=True, is_superuser=True).count()

    context = {
        
        'competition_count':competition_count,
        'competition_list':competition_list,
        'user_list':user_list,
        'user_count': user_count,
        'regular_users_count':regular_users_count,
        'admin_users_count': admin_users_count,

    }

    return render(request, 'frontend/listCompetitions.html', context)


def listUser(request):
    # user_list = User.objects.all()
    
    user_list = User.objects.annotate(competition_count=Count('entry'))
    user_count = user_list.count()
    
    # holidays = HolidayCompetition.objects.all()
    regular_users_count = User.objects.filter(is_staff=False, is_superuser=False).count()
    admin_users_count = User.objects.filter(is_staff=True, is_superuser=True).count()
    context = {
        'user_list':user_list,
        'user_count': user_count,
        'regular_users_count':regular_users_count,
        'admin_users_count': admin_users_count,

    }

    return render(request, 'frontend/listUsers.html', context)


def editCompetition(request, pk):
    # Get the competition object
    competition = get_object_or_404(Competition, pk=pk)

    # Get the current competition images for the carousel
    competition_images = CompetitionImage.objects.filter(competition=competition)

    if request.method == 'POST':
        # Create the forms with POST data and files
        form = CompetitionForm(request.POST, request.FILES, instance=competition)
        image_form = CompetitionImageForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            print("Form is valid.")
            # Save the main competition details
            form.save()

            # Handle multiple images for the carousel
            images = request.FILES.getlist('images')  # 'images' is the MultiFileField name
            for img in images:
                CompetitionImage.objects.create(competition=competition, image=img)

            # Redirect after successful edit
            return redirect('listCompetitions')
        else:
            print(form.errors)
    else:
        # Create the form pre-filled with the competition's data
        form = CompetitionForm(instance=competition)
        image_form = CompetitionImageForm()

    context = {
        'form': form,
        'image_form': image_form,
        'competition': competition,
        'competition_images': competition_images,  # Existing images for display
    }

    return render(request, 'frontend/editCompetition.html', context)

def deleteCompetition(request, pk):
    competition = get_object_or_404(Competition, pk=pk)  # Get the competition or return a 404
    competition.delete()  # Delete the competition
    return redirect('listCompetition')

@csrf_exempt
def deleteImage(request, pk):
    competition = get_object_or_404(CompetitionImage, pk=pk)  # Get the competition or return a 404
    competition.delete()  # Delete the competition
    return HttpResponse('imgae deleted successfuly')


def index(request):
    competitions = Competition.objects.all().order_by('-start_date')[:4]
    context = {
        'competitions': competitions,
    }
    return render(request, 'frontend/index.html', context)


def test(request):
    return render(request, 'frontend/test.html', context={})

def wallet(request):
    pass

def competitions(request):
    competitions = Competition.objects.all()
    return render(request, 'frontend/competitions.html', {'competitions': competitions})


def competition_details(request, competition_id):
    ticket_options = range(2, 21, 2) 
    competitions = Competition.objects.all()
    competition = get_object_or_404(Competition, id=competition_id)
    images = CompetitionImage.objects.filter(competition=competition)

    specs_list = competition.specifications.splitlines()
   
    context = {
        'competition': competition,
        'images': images,
        'ticket_options': ticket_options,
        'competitions': competitions,
        'specs_list': specs_list,
        
    }
    return render(request, 'frontend/competition.html', context)

def holidaycompetitions(request):
    competitions = HolidayCompetition.objects.all()
    return render(request, 'frontend/Holidaycompetitions.html', {'competitions': competitions})


def holicompetition_details(request, holicompetition_id):
    competitions = HolidayCompetition.objects.all()
    competition = get_object_or_404(HolidayCompetition, id=holicompetition_id)
    images = HoliCompetitionImage.objects.filter(competition=competition)

    specs_list = competition.description.splitlines()
   
    context = {
        'competition': competition,
        'images': images,
        'competitions': competitions,
        'specs_list': specs_list,
        
    }
    return render(request, 'frontend/holidaycompedetails.html', context)




@csrf_exempt  # Use with caution, consider your security requirements
def update_basket(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        competition_id = data.get('competition_id')
        ticket_count = data.get('ticket_count')

        competition = get_object_or_404(Competition, id=competition_id)

        if request.user.is_authenticated:
            # Update for authenticated users
            basket_item, created = BasketItem.objects.get_or_create(
                user=request.user,
                competition=competition,
                defaults={'ticket_count': 0}
            )
            basket_item.ticket_count = ticket_count
            basket_item.save()
        else:
            # Update for unauthenticated users
            basket = request.session.get('basket', {})
            basket[competition_id] = ticket_count
            request.session['basket'] = basket

        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)



def add_to_basket(request, id):
    competition = get_object_or_404(Competition, id=id)

    if request.method == 'POST':

        ticket_count = int(request.POST['ticket_count'])

        print('first if')

        if ticket_count > 0 and ticket_count <= (competition.total_tickets - competition.tickets_sold):

            if request.user.is_authenticated:

                basket_item, created = BasketItem.objects.get_or_create(
                    user=request.user,
                    competition=competition,
                    defaults={'ticket_count': ticket_count}
                )

                print('2 if')

                if not created:
                    basket_item.ticket_count += ticket_count
                    basket_item.save()
                    print('3rd if')
            
            else:
                #unauthenticated users
                basket = request.session.get('basket', [])

                #check if item is already in basket
                item_found = next((item for item in basket if item['competition_id'] == competition.id), None)

                if item_found:
                    item_found['ticket_count'] += ticket_count
                else:
                    basket.append({
                        'competition_id': competition.id,
                        'ticket_count': ticket_count,
                    })
                request.session['basket'] = basket
            
        return redirect('competition', competition_id=competition.id)

    return redirect('competition', competition_id=competition.id)



def add_to_baskety(request, id):
    competition = get_object_or_404(HolidayCompetition, id=id)

    if request.method == 'POST':

        ticket_count = int(request.POST['ticket_count'])

        print('first if')

        if ticket_count > 0 and ticket_count <= (competition.total_tickets - competition.tickets_sold):

            if request.user.is_authenticated:

                basket_item, created = BasketItem.objects.get_or_create(
                    user=request.user,
                    holicompetition=competition,
                    defaults={'ticket_count': ticket_count}
                )

                print('2 if')

                if not created:
                    basket_item.ticket_count += ticket_count
                    basket_item.save()
                    print('3rd if')
            
            else:
                #unauthenticated users
                basket = request.session.get('basket', [])

                #check if item is already in basket
                item_found = next((item for item in basket if item['competition_id'] == competition.id), None)

                if item_found:
                    item_found['ticket_count'] += ticket_count
                else:
                    basket.append({
                        'competition_id': competition.id,
                        'ticket_count': ticket_count,
                    })
                request.session['basket'] = basket
            
        return redirect('holicompetition', holicompetition_id=competition.id)

    return redirect('holicompetition', holicompetition_id=competition.id)



def view_basket(request):
    total_cost = 0
    basket_items = []

    if request.user.is_authenticated:
        # Fetch all BasketItem entries for the authenticated user
        basket_items = BasketItem.objects.filter(user=request.user)
        
        # Calculate total cost for authenticated users
        total_cost = sum(
            (item.competition.ticket_price * item.ticket_count if item.competition else 0) +
            (item.holicompetition.ticket_price * item.ticket_count if item.holicompetition else 0)
            for item in basket_items
        )

    else:
        # For unauthenticated users, fetch items from the session
        basket = request.session.get('basket', [])
        
        for item in basket:
            if 'competition_id' in item:
                # Fetch competition item
                competition = get_object_or_404(Competition, id=item['competition_id'])
                total_cost += competition.ticket_price * item['ticket_count']
                basket_items.append({
                    'id': competition.id,
                    'competition': competition,
                    'ticket_count': item['ticket_count'],
                })
            elif 'holicompetition_id' in item:
                # Fetch holiday competition item
                holicompetition = get_object_or_404(HolidayCompetition, id=item['holicompetition_id'])
                total_cost += holicompetition.ticket_price * item['ticket_count']
                basket_items.append({
                    'id': holicompetition.id,
                    'holicompetition': holicompetition,
                    'ticket_count': item['ticket_count'],
                })
    
    return render(request, 'frontend/view_basket.html', {'basket_items': basket_items, 'total_cost': total_cost})

def remove_from_basket(request, item_id):
    item = get_object_or_404(BasketItem, id=item_id)
    item.delete()

    # Optionally add a success message or other logic

    return redirect('view_basket')  # Redirect to the basket view


def token(request):
    consumer_key = 'aWrsHLr8OiGyUlh2SjNVOalHxLOzAJGt'  # Consider using environment variables for sensitive data
    consumer_secret = 'my1Ofjv8W34lyVQx'
    api_URL = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    try:
        # Request access token
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        r.raise_for_status()  # Raise an error for bad responses

        # Parse response
        mpesa_access_token = json.loads(r.text)
        validated_mpesa_access_token = mpesa_access_token.get("access_token")

        if not validated_mpesa_access_token:
            return HttpResponse("Failed to retrieve access token.", status=500)

        # Render template with the token
        return render(request, 'upload_image.html', {"token": validated_mpesa_access_token})

    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    except json.JSONDecodeError:
        # Handle JSON decoding errors
        return HttpResponse("Failed to decode the response.", status=500)
    


def convert_to_usd(total): 
    usdTotal = total/130 
    return usdTotal

def check_out(request):
    # If the user is not authenticated, redirect to login
    if not request.user.is_authenticated:
        # Save the current session basket to session before login
        request.session['basket_before_login'] = request.session.get('basket', [])
        return redirect(reverse('account_login') + '?next=' + reverse('check_out'))

    # Retrieve items in the user's basket
    basket_items = BasketItem.objects.filter(user=request.user)

    # Check if the basket is empty
    if not basket_items:
        return redirect('view_basket')  # Redirect if the basket is empty

    # Calculate the total amount and prepare the item names
    total_amount = 0
    item_names = []

    for item in basket_items:
        if item.competition:
            total_amount += item.competition.ticket_price * item.ticket_count
            item_names.append(item.competition.car_model)
        elif item.holicompetition:
            total_amount += item.holicompetition.ticket_price * item.ticket_count
            item_names.append(item.holicompetition.name)

    item_name_string = ', '.join(item_names)  # Combine item names into a single string
    host = request.get_host()

    # Prepare the PayPal checkout data
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'no_shipping': '2',
        'amount': f"{convert_to_usd(total_amount):.2f}",  
        'item_name': item_name_string,  
        'invoice': str(uuid.uuid4()),  
        'currency_code': 'USD', 
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',  
        'return_url': f'http://{host}{reverse("payment_success")}', 
        'cancel_url': f'http://{host}{reverse("payment_failure")}',  
    }

    # Create the PayPal payment form
    paypal_form = PayPalPaymentsForm(initial=paypal_checkout)


    return render(request, 'frontend/checkout.html', {
        'basket_items': basket_items,
        'Amount': total_amount,
        'paypal_form': paypal_form,
    })


# Stripe configuration
# stripe.api_key = settings.STRIPE_SECRET_KEY

# def create_stripe_checkout_session(request):
#     basket_items = BasketItem.objects.filter(user=request.user)

#         # Create Stripe Checkout session

#     line_items = []
#     for item in basket_items:
#         line_items.append({
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {
#                     'name': item.competition.car_model,

#                 },
#                 'unit_amount': int(item.competition.ticket_price * 100),  # Amount in cents
#             },
#             'quantity': item.ticket_count,
#         })

#     checkout_session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=line_items,
#         mode='payment',
#         success_url='http://127.0.0.1:8000/payment_success/',
#         cancel_url='http://127.0.0.1:8000/payment_failed/',
#     )
#     return checkout_session.id

# def stripe_payment(request):
#   if request.method == 'POST':
#     checkout_session = create_stripe_checkout_session(request)
#     return redirect(checkout_session.url)

def DPO_payment(request):

    if not request.user.is_authenticated:
        return redirect('account_login') 

    basket_items = BasketItem.objects.filter(user=request.user)
    # Initialize the total amount
    total_amount = 0

    # Calculate the total amount considering competition and holicompetition
    for item in basket_items:
        if item.competition:  # Check if the competition exists
            total_amount += item.competition.ticket_price * item.ticket_count
        elif item.holicompetition:  # Check if the holicompetition exists
            total_amount += item.holicompetition.ticket_price * item.ticket_count

    amount = total_amount
    currency = 'KES'  # Customize based on user choice
    transaction_reference = 'test_transaction_reference'  # Use a unique reference for testing
    

    xml_payload = f'<?xml version="1.0" encoding="utf-8"?><API3G><CompanyToken>{DPO_COMPANY_TOKEN}</CompanyToken><Request>createToken</Request><Transaction><PaymentAmount>{amount}</PaymentAmount><PaymentCurrency>{currency}</PaymentCurrency><CompanyRef>49FKEOA</CompanyRef><RedirectURL>https://mydreamcar.africa/payment_success</RedirectURL><BackURL>https://mydreamcar.africa/payment_failed</BackURL><CompanyRefUnique>0</CompanyRefUnique><PTL>5</PTL></Transaction><Services><Service><ServiceType>69232</ServiceType><ServiceDescription>Flight from Nairobi to Diani</ServiceDescription><ServiceDate>2013/12/20 19:00</ServiceDate></Service></Services></API3G>'

    # Send the XML payload to DPO
    headers = {'Content-Type': 'application/xml'}
    response = requests.post(DPO_BASE_URL, headers=headers, data=xml_payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the XML response
        xml_response = ET.fromstring(response.text)
        result = xml_response.find('Result').text
        result_explanation = xml_response.find('ResultExplanation').text
        trans_token = xml_response.find('TransToken').text if xml_response.find('TransToken') is not None else None
        
        # Check if the transaction was created successfully
        if result == '000' and trans_token:
            # Redirect to the payment page
            payment_url = f'https://secure.3gdirectpay.com/payv2.php?ID={trans_token}'
            return redirect(payment_url)
        else:
            return HttpResponse(f"Error: {result_explanation}")  # Display the error
    else:
        return "Failed to connect to DPO test environment"

def stk(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    basket_items = BasketItem.objects.filter(user=request.user)

    # Initialize total_cost to 0
    total_cost = 0

    # Calculate the total cost, ensuring that competition is not None
    for item in basket_items:
        if item.competition:  # Check if competition is not None
            total_cost += item.competition.ticket_price * item.ticket_count
            totalcost = str(round(total_cost))
        elif item.holicompetition:  # Check if holicompetition is not None
            total_cost += item.holicompetition.ticket_price * item.ticket_count
            totalcost = str(round(total_cost))
            
    if request.method == "POST":
        phone = request.POST.get('phone')
        amount = totalcost
        access_token = MpesaAccessToken.get_access_token()

        if not access_token:
            return HttpResponse("Failed to get access token.", status=500)

        api_url = MpesaC2bCredential.api_url
        headers = {"Authorization": f"Bearer {access_token}"}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://django-daraja.vercel.app/add-payment/",
            "AccountReference": "Dream Car",
            "TransactionDesc": "Web Development Charges"
        }

        response = requests.post(api_url, json=request_data, headers=headers)
        response_data = json.loads(response.text)

        print("Response data from M-Pesa API:", response_data)
        checkout_request_id = response_data.get('CheckoutRequestID')

        if response_data.get('ResponseCode') == '0':
            time.sleep(20)  # Simulate a delay for the user to complete the payment

            # Fetch the list of transactions from the callback endpoint
            callback_response = requests.get("https://django-daraja.vercel.app/payments/")
            callback_data = json.loads(callback_response.text)
            callback_data_list = []
            callback_data_list = callback_data["payments"]["rows"]

            # Loop through the callback_data_list to check if the provided checkout_request_id exists
            found = False  # Flag to indicate if we found the ID

            for transaction in callback_data_list:
                if transaction.get("checkoutrequestid") == checkout_request_id:
                    found = True
                    print(f"Checkout Request ID {checkout_request_id} found in the list.")
                    # You can also perform additional actions here, like printing transaction details
                    print("Transaction details:", transaction)
                    
                    if transaction.get("resultcode") == 0:
        
                        # Add tickets to the user's entries
                        basket_items = BasketItem.objects.filter(user=request.user)
                        for item in basket_items:
                            competition = item.competition
                            ticket_count = item.ticket_count
                            
                            # Create entries for the user
                            for _ in range(ticket_count):
                                Entry.objects.create(user=request.user, competition=competition)
                            

                            # Update tickets_sold for the competition
                            competition.tickets_sold += ticket_count
                            competition.save()
                        
                        # Optionally, clear the basket items after processing
                        BasketItem.objects.filter(user=request.user).delete()
                        save_transactions(callback_data_list, request)

                        return redirect(payment_success)
                    else:
                    
                        print(transaction.get("resultdesc"))
                        return redirect(payment_failure)          
                    
            if not found:
                print(f"Checkout Request ID {checkout_request_id} not found in the list.")

        else:
            return redirect('check_out')

    return HttpResponse("Invalid request method.", status=405)


def save_transactions(callback_data_list, request):

    # Extract the list of transactions
    count = 0
    for transaction_data in callback_data_list:
        # Create or update the MpesaTransaction record
        int(count)
        count += 1
        MpesaTransaction.objects.update_or_create(
            checkout_request_id=transaction_data.get("checkoutrequestid",str(count) ),
            defaults={
                'user': request.user,  # You need to define this function
                'merchant_request_id': transaction_data.get("merchantrequestid"),
                'mpesa_receipt_number': transaction_data.get("mpesareceiptnumber"),
                'result_code': transaction_data.get("resultcode"),
                'result_desc': transaction_data.get("resultdesc"),
                'amount': transaction_data.get("amount"),
                'transaction_date': convert_mpesadate(transaction_data.get("transactiondate")),  # Convert to DateTime if needed
                'phone_number': transaction_data.get("phonenumber"),
            }
        )

def convert_mpesadate(date_str):
    if date_str is None:
        return None  # Or handle the missing date appropriately
    try:
        return datetime.datetime.strptime(date_str, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        # Handle the case where date_str is not in the expected format
        return None  # Or log an error, raise an exception, etc.


def payment_success(request):
    # Display a success message to the user
    return render(request, 'frontend/payment_success.html')

def payment_failure(request):
    # Display a failure message to the user
    return render(request, 'frontend/payment_failure.html')
    
    
def base(request):
    return render(request, 'frontend/base.html', context={})

