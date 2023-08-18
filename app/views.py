import json
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests.auth import HTTPBasicAuth
from .credentials import MpesaAccessToken, LipanaMpesaPpassword
from .forms import RegisterForm, LogInForm


# ------------------index page-------------------------------------
def index(request):
    return render(request, 'index.html')


# ------------------register page/View-------------------------------------
def register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

    context = {'form': form}

    return render(request, 'register.html', context=context)


# ------------------login page-------------------------------------
def login(request):
    return render(request, 'login.html')


# ------------------home page-------------------------------------
def home(request):
    return render(request, 'home.html')


def lib(request):
    return render(request, 'libraries.html')


def contact(request):
    return render(request, 'contacts.html')


def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token": validated_mpesa_access_token})


def pay(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Alex Maina",
            "TransactionDesc": "Mika Hub Limited "
        }
        response = requests.post(api_url, json=request_data, headers=headers)
        return HttpResponse("success")

    return render(request, 'pay.html')


def stk(request):
    return render(request, 'pay.html', {'navbar': 'app'})
