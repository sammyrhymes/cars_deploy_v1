from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from .forms import UserUpdateForm, ProfileUpdateForm  # Assuming these forms are correctly defined
from django.contrib.auth.decorators import login_required
from competition.models  import *
from .models import *

import json

from django.http import HttpResponse

import requests
import time
from competition.credentials import LipanaMpesaPpassword, MpesaAccessToken, MpesaC2bCredential


@login_required
def profile(request):
    user = request.user
    # Query all tickets associated with this user
    tickets = Ticket.objects.filter(user=user).select_related('competition')
    
    # Group tickets by competition
    competitions = {}
    for ticket in tickets:
        if ticket.competition not in competitions:
            competitions[ticket.competition] = []
        competitions[ticket.competition].append(ticket.number)
    
    return render(request, 'user/profile.html', {
        'user': user,
        'competitions': competitions
    })
@login_required
def profile_update(request):

    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)
    
    user_profile = request.user.userprofile

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/profile_update.html', context)

def deposit(request):
    # Ensure the user is authenticated
    if request.user.is_authenticated:
        # Get the wallet of the currently logged-in user
        wallet = get_object_or_404(Wallet, user=request.user)

        # Fetch the transactions for the user
        transactions = Transaction.objects.filter(user=request.user)  # ordering by latest transaction first

        print(f"Wallet: {wallet.amount}")
        print(f"Transactions: {transactions}")

        # Context to pass to the template
        context = {
            'wallet': wallet,
            'transactions': transactions,
        }

        # Render the deposit page with the user's wallet and transaction details
        return render(request, 'user/deposit.html', context)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect('login')
    
    
def deposit_stk(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    
    if request.method == "POST":
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        access_token = MpesaAccessToken.get_access_token()

        print(type(phone), type(amount))

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
                                                   
                        wallet = Wallet.objects.get(user=request.user)  # Retrieve the user's wallet
                        wallet.amount += int(amount)  # Add the provided amount to the current wallet amount
                        wallet.save()  # Save the updated wallet instance
                        return redirect('deposit')
                    else:
                        wallet = Wallet.objects.get(user=request.user)
                        print(wallet.amount,wallet)
                        wallet.amount += int(amount)
                        wallet.save()                    
                        # print(transaction.get("resultdesc"))
                        # return redirect(payment_failure) 
                        return redirect('deposit') 
                            
                    
            if not found:
                print(f"Checkout Request ID {checkout_request_id} not found in the list.")

        else:
            return redirect('check_out')

    return HttpResponse("Invalid request method.", status=405)

def deposit(request):

    return render(request,'user/deposit.html',{})